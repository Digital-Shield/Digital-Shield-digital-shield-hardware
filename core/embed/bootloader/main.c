/**
 ******************************************************************************
 * @file    JPEG/JPEG_MJPEG_VideoDecoding/CM7/Src/main.c
 * @author  MCD Application Team
 * @brief   This sample code shows how to use the HW JPEG to Decode an MJPEG video file
 *          using the STM32H7xx HAL API.
 *          This is the main program for Cortex-M7
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2019 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */

/* Includes ------------------------------------------------------------------*/
#include "bootui.h"
#include "common.h"
#include "display.h"
#include "emmc_commands.h"
#include "ff.h"
#include "flash.h"
#include "image.h"
#include "messages.h"
#include "mipi_lcd.h"
#include "mpu.h"
#include "sdram.h"
#include "se.h"
#include "spi.h"
#include "sys.h"
#include "usart.h"
#include "usb.h"
#include <stdio.h>

#include "battery.h"
#include "qspi_flash.h"
#include "random_delays.h"
#include "secbool.h"
#include "stm32h747xx.h"
#include "stm32h7xx_hal_gpio.h"
#include "stm32h7xx_hal_rcc.h"
#include "uart_log.h"
#include "lowlevel.h"

#define MSG_NAME_TO_ID(x) MessageType_MessageType_##x

#define USB_OTG_HS_DATA_FIFO_RAM  (USB_OTG_HS_PERIPH_BASE + 0x20000U)
#define USB_OTG_HS_DATA_FIFO_SIZE (4096U)

#if PRODUCTION
const uint8_t BOOTLOADER_KEY_M = 4;
const uint8_t BOOTLOADER_KEY_N = 7;
#else
const uint8_t BOOTLOADER_KEY_M = 2;
const uint8_t BOOTLOADER_KEY_N = 3;
#endif
const uint8_t * const BOOTLOADER_KEYS[] = {
#if PRODUCTION
#else
    (const uint8_t *)"\x57\x11\x4f\x0a\xa6\x69\xd2\xf8\x37\xe0\x40\xab\x9b\xb5\x1c\x00\x99\x12\x09\xf8\x4b\xfd\x7b\xf0\xf8\x93\x67\x62\x46\xfb\xa2\x4a",
    (const uint8_t *)"\xdc\xae\x8e\x37\xdf\x5c\x24\x60\x27\xc0\x3a\xa9\x51\xbd\x6e\xc6\xca\xa7\xad\x32\xc1\x66\xb1\xf5\x48\xa4\xef\xcd\x88\xca\x3c\xa5",
    (const uint8_t *)"\x77\x29\x12\xab\x61\xd1\xdc\x4f\x91\x33\x32\x5e\x57\xe1\x46\xab\x9f\xac\x17\xa4\x57\x2c\x6f\xcd\xf3\x55\xf8\x00\x36\x10\x00\x04",
#endif
};
DMA2D_HandleTypeDef DMA2D_Handle;

FATFS SDFatFs;  /* File system object for SD card logical drive */
char SDPath[4]; /* SD card logical drive path */

static void bus_fault_enable()
{
    SCB->SHCSR |= SCB_SHCSR_BUSFAULTENA_Msk;
}
static void bus_fault_disable()
{
    SCB->SHCSR &= ~SCB_SHCSR_BUSFAULTENA_Msk;
}

void Error_Display(char* str)
{
    (void)str;
    return;
}

#define USB_IFACE_NUM   0
#define USB_PACKET_SIZE 64

static void usb_init_all(secbool usb21_landing)
{
    usb_dev_info_t dev_info = {
        .device_class = 0x00,
        .device_subclass = 0x00,
        .device_protocol = 0x00,
        .vendor_id = 0x1209,
        .product_id = 0x53c0,
        .release_num = 0x0200,
        .manufacturer = "Digitshield",
        .product = "Digitshield Touch Boot",
        .serial_number = "000000000000000000000000",
        .interface = "Digitshield Interface",
        .usb21_enabled = sectrue,
        .usb21_landing = usb21_landing,
    };

    static uint8_t rx_buffer[USB_PACKET_SIZE];

    static const usb_webusb_info_t webusb_info = {
        .iface_num = USB_IFACE_NUM,
        .ep_in = USB_EP_DIR_IN | 0x01,
        .ep_out = USB_EP_DIR_OUT | 0x01,
        .subclass = 0,
        .protocol = 0,
        .max_packet_len = sizeof(rx_buffer),
        .rx_buffer = rx_buffer,
        .polling_interval = 1,
    };

    usb_init(&dev_info);

    ensure(usb_webusb_add(&webusb_info), NULL);

    usb_start();
}

static secbool bootloader_usb_loop(const vendor_header* const vhdr, const image_header* const hdr)
{ // touch click commented on development board
    // if both are NULL, we don't have a firmware installed
    // let's show a webusb landing page in this case
    usb_init_all((vhdr == NULL && hdr == NULL) ? sectrue : secfalse);

    uint8_t buf[USB_PACKET_SIZE];
    int r;

    for ( ;; )
    {
        while ( true )
        {
            ble_uart_poll();
            // check bluetooth
            if ( USB_PACKET_SIZE == spi_slave_poll(buf) )
            {
                host_channel = CHANNEL_SLAVE;
                break;
            }
            // check usb
            else if ( USB_PACKET_SIZE == usb_webusb_read_blocking(USB_IFACE_NUM, buf, USB_PACKET_SIZE, 5) )
            {
                host_channel = CHANNEL_USB;
                break;
            }
            // no packet, check if power button pressed
            // else if ( ble_power_button_state() == 1 ) // short press
            else if ( ble_power_button_state() == 2 ) // long press
            {
                // give a way to go back to bootloader home page
                ble_power_button_state_clear();
                ui_progress_bar_visible_clear();
                ui_fadeout();
                // ui_bootloader_first(NULL);
                ui_fadein();
                memzero(buf, USB_PACKET_SIZE);
                continue;
            }
            // no packet, no pwer button pressed
            else
            {
                ui_bootloader_page_switch(hdr);
                static uint32_t tickstart = 0;
                if ( (HAL_GetTick() - tickstart) >= 1000 )
                {
                    // ui_title_update();
                    tickstart = HAL_GetTick();
                }
                continue;
            }
        }

        uint16_t msg_id;
        uint32_t msg_size;
        if ( sectrue != msg_parse_header(buf, &msg_id, &msg_size) )
        {
            // invalid header -> discard
            continue;
        }

        switch ( msg_id )
        {
        case MSG_NAME_TO_ID(Initialize): // Initialize
            process_msg_Initialize(USB_IFACE_NUM, msg_size, buf, vhdr, hdr);
            break;
        case MSG_NAME_TO_ID(Ping): // Ping
            process_msg_Ping(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(WipeDevice): // WipeDevice
            ui_fadeout();
            ui_wipe_confirm(hdr);
            ui_fadein();
            int response = ui_input_poll(INPUT_CONFIRM | INPUT_CANCEL, true);
            if ( INPUT_CANCEL == response )
            {
                ui_fadeout();
                // ui_bootloader_first(hdr);
                ui_fadein();
                send_user_abort(USB_IFACE_NUM, "Wipe cancelled");
                break;
            }
            ui_fadeout();
            ui_screen_wipe();
            ui_fadein();
            r = process_msg_WipeDevice(USB_IFACE_NUM, msg_size, buf);
            if ( r < 0 )
            { // error
                ui_fadeout();
                ui_screen_fail();
                ui_fadein();
                usb_stop();
                usb_deinit();
                // while (!touch_click()) {
                // }
                restart();
                return secfalse; // shutdown
            }
            else
            { // success
                ui_fadeout();
                ui_screen_done(0, sectrue);
                ui_fadein();
                usb_stop();
                usb_deinit();
                // while (!touch_click()) {
                // }
                restart();
                return secfalse; // shutdown
            }
            break;
        case MSG_NAME_TO_ID(FirmwareErase): // FirmwareErase
            process_msg_FirmwareErase(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(FirmwareUpload): // FirmwareUpload
            r = process_msg_FirmwareUpload(USB_IFACE_NUM, msg_size, buf);
            if ( r < 0 && r != -4 )
            { // error, but not user abort (-4)
                ui_fadeout();
                ui_screen_fail();
                ui_fadein();
                usb_stop();
                usb_deinit();
                // while (!touch_click()) {
                // }
                restart();
                return secfalse; // shutdown
            }
            else if ( r == 0 )
            { // last chunk received
                // ui_screen_install_progress_upload(1000);
                ui_fadeout();
                ui_screen_done(4, sectrue);
                ui_fadein();
                ui_screen_done(3, secfalse);
                hal_delay(1000);
                ui_screen_done(2, secfalse);
                hal_delay(1000);
                ui_screen_done(1, secfalse);
                hal_delay(1000);
                usb_stop();
                usb_deinit();
                display_clear();
                return sectrue; // jump to firmware
            }
            break;
        case MSG_NAME_TO_ID(FirmwareErase_ex): // erase ble update buffer
            process_msg_FirmwareEraseBLE(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(GetFeatures): // GetFeatures
            process_msg_GetFeatures(USB_IFACE_NUM, msg_size, buf, vhdr, hdr);
            break;
        case MSG_NAME_TO_ID(Reboot): // Reboot
            process_msg_Reboot(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(FirmwareUpdateEmmc): // FirmwareUpdateEmmc
            process_msg_FirmwareUpdateEmmc(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcFixPermission): // EmmcFixPermission
            process_msg_EmmcFixPermission(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcPathInfo): // EmmcPathInfo
            process_msg_EmmcPathInfo(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcFileRead): // EmmcFileRead
            process_msg_EmmcFileRead(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcFileWrite): // EmmcFileWrite
            process_msg_EmmcFileWrite(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcFileDelete): // EmmcFileDelete
            process_msg_EmmcFileDelete(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcDirList): // EmmcDirList
            process_msg_EmmcDirList(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcDirMake): // EmmcDirMake
            process_msg_EmmcDirMake(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcDirRemove): // EmmcDirRemove
            process_msg_EmmcDirRemove(USB_IFACE_NUM, msg_size, buf);
            break;
        default:
            process_msg_unknown(USB_IFACE_NUM, msg_size, buf);
            break;
        }
    }
}

secbool bootloader_usb_loop_factory(const vendor_header* const vhdr, const image_header* const hdr)
{
    // if both are NULL, we don't have a firmware installed
    // let's show a webusb landing page in this case
    usb_init_all((vhdr == NULL && hdr == NULL) ? sectrue : secfalse);

    uint8_t buf[USB_PACKET_SIZE];
    int r;

    for ( ;; )
    {
        r = usb_webusb_read_blocking(USB_IFACE_NUM, buf, USB_PACKET_SIZE, USB_TIMEOUT);
        if ( r != USB_PACKET_SIZE )
        {
            continue;
        }
        host_channel = CHANNEL_USB;

        uint16_t msg_id;
        uint32_t msg_size;
        if ( sectrue != msg_parse_header(buf, &msg_id, &msg_size) )
        {
            // invalid header -> discard
            continue;
        }

        switch ( msg_id )
        {
        case MSG_NAME_TO_ID(Initialize): // Initialize
            process_msg_Initialize(USB_IFACE_NUM, msg_size, buf, vhdr, hdr);
            break;
        case MSG_NAME_TO_ID(Ping): // Ping
            process_msg_Ping(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(GetFeatures): // GetFeatures
            process_msg_GetFeatures(USB_IFACE_NUM, msg_size, buf, vhdr, hdr);
            break;
        case MSG_NAME_TO_ID(DeviceInfoSettings): // DeviceInfoSettings
            process_msg_DeviceInfoSettings(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(GetDeviceInfo): // GetDeviceInfo
            process_msg_GetDeviceInfo(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(ReadSEPublicKey): // ReadSEPublicKey
            process_msg_ReadSEPublicKey(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(WriteSEPublicCert): // WriteSEPublicCert
            process_msg_WriteSEPublicCert(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(ReadSEPublicCert): // ReadSEPublicCert
            process_msg_ReadSEPublicCert(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(SESignMessage): // SESignMessage
            process_msg_SESignMessage(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(Reboot): // Reboot
            process_msg_Reboot(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcFixPermission): // EmmcFixPermission
            process_msg_EmmcFixPermission(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcPathInfo): // EmmcPathInfo
            process_msg_EmmcPathInfo(USB_IFACE_NUM, msg_size, buf);
            break;
        // case MSG_NAME_TO_ID(EmmcFileRead): // EmmcFileRead
        //   process_msg_EmmcFileRead(USB_IFACE_NUM, msg_size, buf);
        //   break;
        // case MSG_NAME_TO_ID(EmmcFileWrite): // EmmcFileWrite
        //   process_msg_EmmcFileWrite(USB_IFACE_NUM, msg_size, buf);
        //   break;
        // case MSG_NAME_TO_ID(EmmcFileDelete): // EmmcFileDelete
        //   process_msg_EmmcFileDelete(USB_IFACE_NUM, msg_size, buf);
        //   break;
        case MSG_NAME_TO_ID(EmmcDirList): // EmmcDirList
            process_msg_EmmcDirList(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcDirMake): // EmmcDirMake
            process_msg_EmmcDirMake(USB_IFACE_NUM, msg_size, buf);
            break;
        case MSG_NAME_TO_ID(EmmcDirRemove): // EmmcDirRemove
            process_msg_EmmcDirRemove(USB_IFACE_NUM, msg_size, buf);
            break;
        default:
            process_msg_unknown(USB_IFACE_NUM, msg_size, buf);
            break;
        }
    }
    return sectrue;
}

static secbool handle_flash_ecc_error = secfalse;
static void set_handle_flash_ecc_error(secbool val)
{
    handle_flash_ecc_error = val;
}
secbool load_vendor_header_keys(const uint8_t* const data, vendor_header* const vhdr)
{
    return load_vendor_header(data, BOOTLOADER_KEY_M, BOOTLOADER_KEY_N, BOOTLOADER_KEYS, vhdr);
}

// static
secbool check_vendor_header_lock(const vendor_header* const vhdr)
{
    uint8_t lock[FLASH_OTP_BLOCK_SIZE];
    ensure(flash_otp_read(FLASH_OTP_BLOCK_VENDOR_HEADER_LOCK, 0, lock, FLASH_OTP_BLOCK_SIZE), NULL);
    if ( 0 == memcmp(
                  lock,
                  "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
                  "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF",
                  FLASH_OTP_BLOCK_SIZE
              ) )
    {
        return sectrue;
    }
    uint8_t hash[32];
    vendor_header_hash(vhdr, hash);
    return sectrue * (0 == memcmp(lock, hash, 32));
}

static secbool validate_firmware_headers(vendor_header* const vhdr, image_header* const hdr)
{
    set_handle_flash_ecc_error(sectrue);
    secbool result = secfalse;
    while ( true )
    {
        // check
        if ( sectrue != load_vendor_header_keys((const uint8_t*)FIRMWARE_START, vhdr) )
            break;

        if ( sectrue != check_vendor_header_lock(vhdr) )
            break;

        if ( sectrue != load_image_header(
                            (const uint8_t*)(FIRMWARE_START + vhdr->hdrlen), FIRMWARE_IMAGE_MAGIC,
                            FIRMWARE_IMAGE_MAXSIZE, vhdr->vsig_m, vhdr->vsig_n, vhdr->vpub, hdr
                        ) )
            break;

        // passed, return true
        result = sectrue;
        break;
    }
    set_handle_flash_ecc_error(secfalse);
    return result;
}

static secbool validate_firmware_code(vendor_header* const vhdr, image_header* const hdr)
{
    set_handle_flash_ecc_error(sectrue);
    secbool result =
        check_image_contents(hdr, IMAGE_HEADER_SIZE + vhdr->hdrlen, FIRMWARE_SECTORS, FIRMWARE_SECTORS_COUNT);
    set_handle_flash_ecc_error(secfalse);
    return result;
}

int main(void)
{
    volatile uint32_t stay_in_bootloader_flag = *STAY_IN_FLAG_ADDR;
    bool serial_set = false, cert_set = false;

    // use log
    uart_log_init();
    printf("hello, bootloader\n");

    HAL_Init();

    SystemCoreClockUpdate();

    /* Enable the CPU Cache */
    // cpu_cache_enable();

    mpu_config_bootloader();

    random_delays_init();
    motor_init();

    // #0 hold system power pin
    // 1. the device is powered, if user push `power button` then release
    // 2. the device is not shutdown, if user connect USB then disconnect USB
    __HAL_RCC_GPIOC_CLK_ENABLE();
    GPIO_InitTypeDef sys_power_on;
    sys_power_on.Pin = GPIO_PIN_1;
    sys_power_on.Mode = GPIO_MODE_OUTPUT_PP;
    sys_power_on.Pull = GPIO_PULLDOWN;
    sys_power_on.Speed = GPIO_SPEED_MEDIUM;

    // pull up power pin
    HAL_GPIO_Init(GPIOC, &sys_power_on);
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_SET);

    // read PJ4 GPIO state, if high, device is powered by battery, otherwise powered by USB
    // __HAL_RCC_GPIOJ_CLK_ENABLE();
    // GPIO_InitTypeDef power_key;
    // power_key.Pin = GPIO_PIN_4;
    // power_key.Mode = GPIO_MODE_INPUT;
    // power_key.Pull = GPIO_NOPULL;
    // power_key.Speed = GPIO_SPEED_FREQ_LOW;
    // HAL_GPIO_Init(GPIOJ, &power_key);
    // if ( HAL_GPIO_ReadPin(GPIOJ, GPIO_PIN_4) != GPIO_PIN_RESET )
    // {
    //     // here can test battery state of charge, if low battery can shutdown immediately
    // }
    // HAL_GPIO_DeInit(GPIOJ, GPIO_PIN_4);

    bus_fault_enable();
    /* Initialize the QSPI */
    qspi_flash_init();
    qspi_flash_config();
    qspi_flash_memory_mapped();

    // bus_fault_disable();
    // /* Initialize the LCD */
    // TODO: add boot ui
    // touch_init();
    // lcd_para_init(480, 800, LCD_PIXEL_FORMAT_RGB565);
    // display_clear();

    // device_para_init(); // TODO: need debug.
    if (!serial_set) {
      serial_set = device_serial_set();
      serial_set = true; // TODO: need debug.
    }

    // se_init();
    if (!cert_set) { // if se certificate is not set
    //   uint32_t cert_len = 0;
    //   cert_set = se_get_certificate_len(&cert_len);
      cert_set = true; // TODO: need debug.
    }

    if (!serial_set || !cert_set) {
      display_clear();
      device_set_factory_mode(true);
      ui_bootloader_factory();
      if (bootloader_usb_loop_factory(NULL, NULL) != sectrue) {
        return 1;
      }
    }

    wait_random();
    ensure_emmcfs(emmc_fs_init(), "emmc_fs_init");
    ensure_emmcfs(emmc_fs_mount(true, false), "emmc_fs_mount");

    BLE_CTL_PIN_INIT();
    ble_function_on();

    secbool stay_in_bootloader = secfalse; // flag to stay in bootloader
    if ( stay_in_bootloader_flag == STAY_IN_BOOTLOADER_FLAG )
    {
        *STAY_IN_FLAG_ADDR = 0;
        stay_in_bootloader = sectrue;
    }

    // stay_in_bootloader = sectrue;

    vendor_header vhdr;
    image_header hdr;
    // check stay_in_bootloader flag
    if ( stay_in_bootloader == sectrue )
    {
        display_clear();
        if ( sectrue == validate_firmware_headers(&vhdr, &hdr) )
        {
            ui_bootloader_first(&hdr);
            if ( bootloader_usb_loop(&vhdr, &hdr) != sectrue )
            {
                return 1;
            }
        }
        else
        {
            ui_bootloader_first(NULL);
            if ( bootloader_usb_loop(NULL, NULL) != sectrue )
            {
                return 1;
            }
        }
        if ( sectrue == validate_firmware_headers(&vhdr, &hdr) )
        {
            // ui_bootloader_first(&hdr);
            if ( bootloader_usb_loop(&vhdr, &hdr) != sectrue )
            {
                return 1;
            }
        }
        else
        {
            // ui_bootloader_first(NULL);
            if ( bootloader_usb_loop(NULL, NULL) != sectrue )
            {
                return 1;
            }
        }
    }

    // check if firmware valid
    if ( sectrue == validate_firmware_headers(&vhdr, &hdr) )
    {
        if ( sectrue == validate_firmware_code(&vhdr, &hdr) )
        {
            // __asm("nop"); // all good, do nothing
        }
        else
        {
            display_clear();
            ui_bootloader_first(&hdr);
            // if (bootloader_usb_loop(&vhdr, &hdr) != sectrue) {
            //   return 1;
            // }
        }
    }
    else
    {
        display_clear();
        ui_bootloader_first(NULL);
        if ( bootloader_usb_loop(NULL, NULL) != sectrue )
        {
            return 1;
        }
    }

    // check if firmware valid again to make sure
    // ensure(validate_firmware_headers(&vhdr, &hdr), "invalid firmware header");
    // ensure(validate_firmware_code(&vhdr, &hdr), "invalid firmware code");

    // if all VTRUST flags are unset = ultimate trust => skip the procedure
    // if ((vhdr.vtrust & VTRUST_ALL) != VTRUST_ALL) {
    //   // ui_fadeout();  // no fadeout - we start from black screen
    //   ui_screen_boot(&vhdr, &hdr);
    //   ui_fadein();

    //   int delay = (vhdr.vtrust & VTRUST_WAIT) ^ VTRUST_WAIT;
    //   if (delay > 1) {
    //     while (delay > 0) {
    //       ui_screen_boot_wait(delay);
    //       hal_delay(1000);
    //       delay--;
    //     }
    //   } else if (delay == 1) {
    //     hal_delay(1000);
    //   }

    //   if ((vhdr.vtrust & VTRUST_CLICK) == 0) {
    //     ui_screen_boot_click();
    //     while (touch_read() == 0)
    //       ;
    //   }
    //   display_clear();
    // }

    // mpu_config_firmware();
    // jump_to_unprivileged(FIRMWARE_START + vhdr.hdrlen + IMAGE_HEADER_SIZE);
    bus_fault_disable();
    mpu_config_off();
    jump_to(FIRMWARE_START + vhdr.hdrlen + IMAGE_HEADER_SIZE);
    return 0;
}
