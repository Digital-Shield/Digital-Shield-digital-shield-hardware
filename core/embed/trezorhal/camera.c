#include "camera.h"
#include STM32_HAL_H

#include "stm32h7xx_hal_gpio.h"
#include "stm32h7xx_hal_dcmi.h"
#include "stm32h7xx_hal_dma.h"
#include "stm32h7xx_hal_dma_ex.h"
#include "stm32h7xx_hal_mdma.h"
#include "stm32h7xx_hal_ltdc.h"

#include <stdbool.h>
#include <string.h>
#include <stdint.h>
#include <stdio.h>

#include "sdram.h"
#include "secbool.h"
#include "gc0308.h"
#include "i2c.h"
#include "device.h"
#include "power_manager.h"

#include "quirc.h"

// we initialize quiric struct directly in this file, not in quirc module
// so include `internal` header file
#include "quirc_internal.h"

// clang-format off
/*
        ┌─────────────────────────────┐
        │                             │
        │         Camera              │
        │                             │
        └──────────────┬──────────────┘
                       │
                       │
                       │
                       ▼
        ┌──────────────────────────────┐
        │                              │
        │   SRam in D2 domain          │
        │                              │
        │   For speed up capturing     │
        │                              │
        └───────────────┬──────────────┘
                        │
            Clip        │
                        │
            640 x 480   │
                        │
            to          │
                        │
            400 x 400   │
                        │
        ┌───────────────▼─────────────┐
        │                             │
        │    Camera Buffer            │
        │                             │
        └──────────────┬──────────────┘
                       │
           rotate      │  current version gc0308 image direction not fit the screen
                       │
                       │  coming version do not need this operation
                       │
                       ▼
       ┌────────────────────────────────┐
       │                                │
       │    Image Buffer                │
       │                                │
       │    For directly draw on screen │
       │                                │
       └───────────────┬────────────────┘
                       │
          rgb565 -> gray
                       │
      ┌────────────────▼─────────────────┐
      │                                  │
      │   Gray image buffer              │
      │                                  │
      │   For QRCode decode              │
      │                                  │
      │                                  │
      └──────────────────────────────────┘

*/
// clang-format on
// debug for qrcode scan
#define CAMERA_SHOW_GRAY 0

// the first version of sensor out image need rotate
// TODO: remove this micro later
#define SENSOR_OUT_IMAGE_NEED_ROTATE 0

// camera power module control pin PK2
#define CAMERA_POWER_GPIO_CLK_ENABLE() __HAL_RCC_GPIOK_CLK_ENABLE()
#define CAMERA_POWER_GPIO_PORT GPIOK
#define CAMERA_POWER_GPIO_PIN GPIO_PIN_2

#define CAMERA_POWER_ON() do {                                                      \
  if (PCB_IS_V10()) {                                                               \
    HAL_GPIO_WritePin(CAMERA_POWER_GPIO_PORT, CAMERA_POWER_GPIO_PIN, GPIO_PIN_SET); \
  } else if (PCB_IS_V11()) {                                                        \
    pm_power_up(POWER_MODULE_CAMERA);                                               \
  }                                                                                 \
}while(0)
#define CAMERA_POWER_OFF() do {                                                      \
  if (PCB_IS_V10()) {                                                                \
    HAL_GPIO_WritePin(CAMERA_POWER_GPIO_PORT, CAMERA_POWER_GPIO_PIN, GPIO_PIN_RESET); \
  } else if (PCB_IS_V11()) {                                                          \
    pm_power_down(POWER_MODULE_CAMERA);                                               \
  }                                                                                   \
}while(0)
// camera  work state pin PJ14
#define CAMERA_WORK_STATE_GPIO_CLK_ENABLE() __HAL_RCC_GPIOJ_CLK_ENABLE()
#define CAMERA_WORK_STATE_GPIO_PORT GPIOJ
#define CAMERA_WORK_STATE_GPIO_PIN GPIO_PIN_14

// pcb v1.0 camera hard reset pin PJ7
#define CAMERA_HW_RESET_GPIO_CLK_ENABLE() __HAL_RCC_GPIOJ_CLK_ENABLE()
#define CAMERA_HW_RESET_GPIO_PORT GPIOJ
#define CAMERA_HW_RESET_GPIO_PIN GPIO_PIN_7

// pcb v1.0 camera hard reset pin PE2
#define V11_CAMERA_HW_RESET_GPIO_CLK_ENABLE() __HAL_RCC_GPIOE_CLK_ENABLE()
#define V11_CAMERA_HW_RESET_GPIO_PORT GPIOE
#define V11_CAMERA_HW_RESET_GPIO_PIN GPIO_PIN_2

// pcb v1.0 camera led pin PJ6
#define CAMERA_LED_GPIO_CLK_ENABLE() __HAL_RCC_GPIOJ_CLK_ENABLE()
#define CAMERA_LED_GPIO_PORT GPIOJ
#define CAMERA_LED_GPIO_PIN GPIO_PIN_6

// pcb v1.1 camera led pin PD5
#define V11_CAMERA_LED_GPIO_CLK_ENABLE() __HAL_RCC_GPIOD_CLK_ENABLE()
#define V11_CAMERA_LED_GPIO_PORT GPIOD
#define V11_CAMERA_LED_GPIO_PIN GPIO_PIN_5

#define CAMERA_CAPTURE_BUFFER 0x30020000 // sram2 in D2

#define GC0308_RGB565 1 // rgb565 bytes in gc0308 is reversed

static bool camera_power = false;
static uint32_t line = 0;
static struct quirc __quirc__;
static struct quirc *qr = &__quirc__;
static DCMI_HandleTypeDef hdcmi = {0};
static MDMA_HandleTypeDef hmdma;
extern LTDC_HandleTypeDef hlcd_ltdc;

// local functions
/// camera functions
static void camera_power_init(void);
static void camera_led_init(void);
static void camera_hardware_reset(void);
static void camera_work_normal(void);
static void camera_mdma_init(void);
static HAL_StatusTypeDef camera_start_dma(DCMI_HandleTypeDef *hdcmi,
                                   uint32_t DCMI_Mode, uint32_t pData);
secbool camera_quric_resize(struct quirc *q, int w, int h);
static void lcd_layer2_init(void);

/// DCMI functions
static void DCMI_MspInit(DCMI_HandleTypeDef *hdcmi);
static HAL_StatusTypeDef MX_DCMI_Init(DCMI_HandleTypeDef* hdcmi);
static void DCMI_MspDeInit(DCMI_HandleTypeDef *hdcmi);

#if CAMERA_SHOW_GRAY
static void gray_to_rgb565(void);
#define CAMERA_TEST_BUFFER (FMC_SDRAM_USER_HEAP_ADDRESS + FMC_SDRAM_USER_HEAP_LEN)
#endif

static struct {
  uint32_t x0;
  uint32_t x1;
  uint32_t y0;
  uint32_t y1;
  uint32_t width;
  uint32_t height;
} window = {0}; // camera cut window


volatile uint32_t qr_status = 0;
enum {
  QR_NONE,
  QR_MAKING_GRAYSCALE,
  QR_GRAYSCALE,
  QR_CODE,
};

#define CAMERA_FRAME_WIDTH 640
#define CAMERA_FRAME_HEIGHT 480

/// exported functions
secbool camera_init(int width, int height) {
  window.width = width;
  window.height = height;
  window.x0 = (CAMERA_FRAME_WIDTH - width ) / 2;
  window.x1 = window.x0 + width;
  window.y0 = (CAMERA_FRAME_HEIGHT - height) / 2;
  window.y1 = window.y0 + height;
  line = 0;

  // clip 640x480 to 400x400
  camera_mdma_init();

  // directly draw on lcd
  lcd_layer2_init();

  // init quric
  camera_quric_resize(qr, width, height);
  // make camera in normal mode
  camera_work_normal();
  // power on camera module
  if (PCB_IS_V10()) {
    camera_power_init();
  }
  CAMERA_POWER_ON();
  // hardware reset
  camera_hardware_reset();

  // gc0308 initialize
  int id = 0;
  printf("gc0308 probing ...\n");
  i2c4_lock();
  if (gc0308_read_id(&id) == 0 && id == GC0308_ID) {
    printf("gc0308 found\n");
    gc0308_init();
  }
  i2c4_unlock();

  // dcmi initialize
  DCMI_MspInit(&hdcmi);

  MX_DCMI_Init(&hdcmi);
  camera_power = true;
  qr_status = QR_NONE;
  return sectrue;
}

void camera_deinit(void) {
  if (camera_power) {
    qr_status = QR_NONE;
    camera_power = false;
    HAL_DCMI_DeInit(&hdcmi);
    DCMI_MspDeInit(&hdcmi);
    HAL_MDMA_DeInit(&hmdma);
    memset(&window, 0, sizeof(window));
    CAMERA_POWER_OFF();
  }
}

void camera_start(void) {
  camera_start_dma(&hdcmi, DCMI_MODE_CONTINUOUS, CAMERA_CAPTURE_BUFFER);
}

void camera_suspend(void) {
  HAL_DCMI_Suspend(&hdcmi);
}

void camera_resume(void) {
  HAL_DCMI_Resume(&hdcmi);
}

void camera_stop(void) {
  HAL_DCMI_Stop(&hdcmi);
}

void camera_hide(void) {
  __HAL_LTDC_LAYER_DISABLE(&hlcd_ltdc, LTDC_LAYER_2);
  __HAL_LTDC_RELOAD_IMMEDIATE_CONFIG(&hlcd_ltdc);
  camera_suspend();
  qr_status = QR_NONE;
}

void camera_show(void) {
  camera_resume();
  lcd_layer2_init();
}

void camera_led_on(void) {
    // camera led on
  camera_led_init();
  if (PCB_IS_V10()) {
    HAL_GPIO_WritePin(CAMERA_LED_GPIO_PORT, CAMERA_LED_GPIO_PIN, GPIO_PIN_SET);
  } else if(PCB_IS_V11()){
    HAL_GPIO_WritePin(V11_CAMERA_LED_GPIO_PORT, V11_CAMERA_LED_GPIO_PIN, GPIO_PIN_SET);
  }
}

void camera_led_off(void) {
  // camera led off
  if (PCB_IS_V10()) {
    HAL_GPIO_WritePin(CAMERA_LED_GPIO_PORT, CAMERA_LED_GPIO_PIN, GPIO_PIN_RESET);
  } else if(PCB_IS_V11()){
    HAL_GPIO_WritePin(V11_CAMERA_LED_GPIO_PORT, V11_CAMERA_LED_GPIO_PIN, GPIO_PIN_RESET);
  }
}

secbool camera_is_power_on(void) { return camera_power; }
secbool camera_is_captured(void) { return qr_status == QR_GRAYSCALE; }

/// local functions
void camera_hardware_reset(void) {
  GPIO_InitTypeDef gpio;
  GPIO_TypeDef* port = NULL;
  uint32_t pin = 0;
  if (PCB_IS_V10()) {
    CAMERA_HW_RESET_GPIO_CLK_ENABLE();
    port = CAMERA_HW_RESET_GPIO_PORT;
    pin = CAMERA_HW_RESET_GPIO_PIN;
  } else if (PCB_IS_V11()) {
    V11_CAMERA_HW_RESET_GPIO_CLK_ENABLE();
    port = V11_CAMERA_HW_RESET_GPIO_PORT;
    pin = V11_CAMERA_HW_RESET_GPIO_PIN;
  }

  gpio.Mode = GPIO_MODE_OUTPUT_PP;
  gpio.Pull = GPIO_PULLUP;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;
  gpio.Pin = pin;
  HAL_GPIO_Init(port, &gpio);

  // hard reset camera
  HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
  HAL_Delay(10);
  // release reset
  HAL_GPIO_WritePin(port, pin, GPIO_PIN_SET);
  HAL_Delay(10);
}

void camera_work_normal(void) {
  GPIO_InitTypeDef gpio;

  CAMERA_WORK_STATE_GPIO_CLK_ENABLE();

  gpio.Pin = CAMERA_WORK_STATE_GPIO_PIN;
  gpio.Mode = GPIO_MODE_OUTPUT_PP;
  gpio.Pull = GPIO_PULLDOWN;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(CAMERA_WORK_STATE_GPIO_PORT, &gpio);

  // 0: normal mode, 1: standby mode
  HAL_GPIO_WritePin(CAMERA_WORK_STATE_GPIO_PORT, GPIO_PIN_14, GPIO_PIN_RESET);
}

// directly draw on lcd
void lcd_layer2_init(void) {
  // need config `LTDC`
  hlcd_ltdc.Instance = LTDC;
  LTDC_LayerCfgTypeDef layer;
  uint32_t x0 = (480 - window.width) / 2;
  uint32_t x1 = x0 + window.width;
  uint32_t y0 = (800 - window.height) / 2;
  uint32_t y1 = y0 + window.height;

  // TODO: use dma fill buffer, reduce cpu load
  memset((void*)FMC_SDRAM_IMAGE_BUFFER_ADDRESS, 0xFF, window.width * window.height * 2);
#if CAMERA_SHOW_GRAY
  memset((void*)CAMERA_TEST_BUFFER, 0xFF, window.width * window.height * 2);
#endif


  layer.WindowX0 = x0;
  layer.WindowX1 = x1;
  layer.WindowY0 = y0;
  layer.WindowY1 = y1;
  layer.PixelFormat = LTDC_PIXEL_FORMAT_RGB565;
  layer.Alpha = 255;
  layer.Alpha0 = 0;
  layer.BlendingFactor1 = LTDC_BLENDING_FACTOR1_PAxCA;
  layer.BlendingFactor2 = LTDC_BLENDING_FACTOR2_PAxCA;
#if CAMERA_SHOW_GRAY
  layer.FBStartAdress = CAMERA_TEST_BUFFER;
#else
  layer.FBStartAdress = FMC_SDRAM_IMAGE_BUFFER_ADDRESS;
#endif
  layer.ImageWidth = window.width;
  layer.ImageHeight = window.height;
  layer.Backcolor.Blue = 0;
  layer.Backcolor.Green = 0;
  layer.Backcolor.Red = 0;
  HAL_LTDC_ConfigLayer(&hlcd_ltdc, &layer, LTDC_LAYER_2);
  __HAL_LTDC_LAYER_ENABLE(&hlcd_ltdc, LTDC_LAYER_2);
  (void)HAL_LTDC_ConfigColorKeying_NoReload(&hlcd_ltdc, 0x00, LTDC_LAYER_2);
  (void)HAL_LTDC_EnableColorKeying_NoReload(&hlcd_ltdc, LTDC_LAYER_2);
}

// copied from `quric.c`
secbool camera_quric_resize(struct quirc *q, int w, int h) {
  uint8_t *image = NULL;
  quirc_pixel_t *pixels = NULL;
  size_t num_vars;
  size_t vars_byte_size;
  struct quirc_flood_fill_vars *vars = NULL;

  /*
   * XXX: w and h should be size_t (or at least unsigned) as negatives
   * values would not make much sense. The downside is that it would break
   * both the API and ABI. Thus, at the moment, let's just do a sanity
   * check.
   */
  if (w < 0 || h < 0) goto fail;

  // maybe we don't need fixed address? just dynamicly allocate
  image = (uint8_t *)(FMC_SDRAM_QUIRC_BUFFER_ADDRESS);

  /* compute the "old" (i.e. currently allocated) and the "new"
     (i.e. requested) image dimensions */
  // size_t olddim = q->w * q->h;
  size_t newdim = w * h;
  // size_t min = (olddim < newdim ? olddim : newdim);

  /*
   * copy the data into the new buffer, avoiding (a) to read beyond the
   * old buffer when the new size is greater and (b) to write beyond the
   * new buffer when the new size is smaller, hence the min computation.
   */
  // we don't need to copy the data, just use the new buffer,
  // we convert image from rgb565 to grayscale when capture new frame
  // (void)memcpy(image, q->image, min);

  /* alloc a new buffer for q->pixels if needed */
  if (!QUIRC_PIXEL_ALIAS_IMAGE) {
    pixels = calloc(newdim, sizeof(quirc_pixel_t));
    if (!pixels) goto fail;
  }

  /*
   * alloc the work area for the flood filling logic.
   *
   * the size was chosen with the following assumptions and observations:
   *
   * - rings are the regions which requires the biggest work area.
   * - they consumes the most when they are rotated by about 45 degree.
   *   in that case, the necessary depth is about (2 * height_of_the_ring).
   * - the maximum height of rings would be about 1/3 of the image height.
   */

  if ((size_t)h * 2 / 2 != h) {
    goto fail; /* size_t overflow */
  }
  num_vars = (size_t)h * 2 / 3;
  if (num_vars == 0) {
    num_vars = 1;
  }

  vars_byte_size = sizeof(*vars) * num_vars;
  if (vars_byte_size / sizeof(*vars) != num_vars) {
    goto fail; /* size_t overflow */
  }
  vars = (void *)(FMC_SDRAM_QUIRC_BUFFER_ADDRESS + 256 * 1024);

  /* alloc succeeded, update `q` with the new size and buffers */
  q->w = w;
  q->h = h;
  // free(q->image);
  q->image = image;
  if (!QUIRC_PIXEL_ALIAS_IMAGE) {
    free(q->pixels);
    q->pixels = pixels;
  }
  // free(q->flood_fill_vars);
  q->flood_fill_vars = vars;
  q->num_flood_fill_vars = num_vars;

  return 0;

fail:
  // free(image);
  // free(pixels);
  // free(vars);
  return secfalse;
}

static void camera_mdma_init(void) {
  __HAL_RCC_MDMA_CLK_ENABLE();
  hmdma.Instance = MDMA_Channel1;
  hmdma.Init.Request = MDMA_REQUEST_SW;
  hmdma.Init.TransferTriggerMode = MDMA_BLOCK_TRANSFER;
  hmdma.Init.Priority = MDMA_PRIORITY_HIGH;
#if GC0308_RGB565
  hmdma.Init.Endianness = MDMA_LITTLE_BYTE_ENDIANNESS_EXCHANGE;
#else
  hmdma.Init.Endianness = MDMA_LITTLE_ENDIANNESS_PRESERVE;
#endif
  hmdma.Init.SourceInc = MDMA_SRC_INC_WORD;
  hmdma.Init.DestinationInc = MDMA_DEST_INC_WORD;
  hmdma.Init.SourceDataSize = MDMA_SRC_DATASIZE_WORD;
  hmdma.Init.DestDataSize = MDMA_DEST_DATASIZE_WORD;
  hmdma.Init.DataAlignment = MDMA_DATAALIGN_PACKENABLE;
  hmdma.Init.SourceBurst = MDMA_SOURCE_BURST_4BEATS;
  hmdma.Init.DestBurst = MDMA_DEST_BURST_4BEATS;
  hmdma.Init.BufferTransferLength = 128;
  hmdma.Init.SourceBlockAddressOffset = 0;
  hmdma.Init.DestBlockAddressOffset = 0;

  HAL_MDMA_Init(&hmdma);
}

static void DCMI_DMAXferCplt(DMA_HandleTypeDef *hdma)
{
  uint32_t tmp ;
  DCMI_HandleTypeDef *hdcmi = (DCMI_HandleTypeDef *)((DMA_HandleTypeDef *)hdma)->Parent;
  uint32_t src = 0;
  uint32_t dst = 0;

  if (hdcmi->XferCount != 0U)
  {
    /* Update memory 0 address location */
    tmp = ((((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->CR) & DMA_SxCR_CT);
    if (((hdcmi->XferCount % 2U) == 0U) && (tmp != 0U))
    {
      src = tmp = ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M0AR;
      (void)HAL_DMAEx_ChangeMemory(hdcmi->DMA_Handle, (tmp + (8U * hdcmi->XferSize)), MEMORY0);
      hdcmi->XferCount--;
    }
    /* Update memory 1 address location */
    else if ((((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->CR & DMA_SxCR_CT) == 0U)
    {
      src = tmp = ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M1AR;
      (void)HAL_DMAEx_ChangeMemory(hdcmi->DMA_Handle, (tmp + (8U * hdcmi->XferSize)), MEMORY1);
      hdcmi->XferCount--;
    }
    else
    {
      /* Nothing to do */
    }
  }
  /* Update memory 0 address location */
  else if ((((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->CR & DMA_SxCR_CT) != 0U)
  {
    src = ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M0AR;
    ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M0AR = hdcmi->pBuffPtr;
  }
  /* Update memory 1 address location */
  else if ((((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->CR & DMA_SxCR_CT) == 0U)
  {
    src = ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M1AR;
    tmp = hdcmi->pBuffPtr;
    ((DMA_Stream_TypeDef *)(hdcmi->DMA_Handle->Instance))->M1AR = (tmp + (4U * hdcmi->XferSize));
    hdcmi->XferCount = hdcmi->XferTransferNumber;
  }

  // (void)src;(void)dst;
  // TODO: use senser corp image
  if (line >= window.y0 && line < window.y1) {
#if SENSOR_OUT_IMAGE_NEED_ROTATE
	  dst = FMC_SDRAM_CAMERA_BUFFER_ADDRESS + (line - window.y0) * window.width * 2;
#else
    dst = FMC_SDRAM_IMAGE_BUFFER_ADDRESS + (line - window.y0) * window.width * 2;
#endif
	  src = src + (window.x0) * 2;
	  //memcpy(dst, src, window.width * 2);
    HAL_MDMA_Start(&hmdma, src, dst, window.width * 2, 1);
    HAL_MDMA_PollForTransfer(&hmdma, HAL_MDMA_FULL_TRANSFER, 1000);
  }
  line ++;
  if (line == CAMERA_FRAME_HEIGHT) {
    line = 0;
    __HAL_DCMI_ENABLE_IT(hdcmi, DCMI_IT_FRAME);
  }
}
static void DCMI_DMAError(DMA_HandleTypeDef *hdma) {
  DCMI_HandleTypeDef *hdcmi =
      (DCMI_HandleTypeDef *)((DMA_HandleTypeDef *)hdma)->Parent;

  if (hdcmi->DMA_Handle->ErrorCode != HAL_DMA_ERROR_FE) {
    /* Initialize the DCMI state*/
    hdcmi->State = HAL_DCMI_STATE_READY;

    /* Set DCMI Error Code */
    hdcmi->ErrorCode |= HAL_DCMI_ERROR_DMA;
  }

  /* DCMI error Callback */
#if (USE_HAL_DCMI_REGISTER_CALLBACKS == 1)
  /*Call registered DCMI error callback*/
  hdcmi->ErrorCallback(hdcmi);
#else
  HAL_DCMI_ErrorCallback(hdcmi);
#endif /* USE_HAL_DCMI_REGISTER_CALLBACKS */
}

static void DCMI_Abort(DMA_HandleTypeDef *hdma) {
  printf("DCMI abort\n");
}

HAL_StatusTypeDef camera_start_dma(DCMI_HandleTypeDef *hdcmi,
                                   uint32_t DCMI_Mode, uint32_t pData) {
  /* Initialize the second memory address */
  uint32_t SecondMemAddress;

  /* Check function parameters */
  assert_param(IS_DCMI_CAPTURE_MODE(DCMI_Mode));

  /* Process Locked */
  __HAL_LOCK(hdcmi);

  /* Lock the DCMI peripheral state */
  hdcmi->State = HAL_DCMI_STATE_BUSY;

  /* Enable DCMI by setting DCMIEN bit */
  __HAL_DCMI_ENABLE(hdcmi);

  /* Configure the DCMI Mode */
  hdcmi->Instance->CR &= ~(DCMI_CR_CM);
  hdcmi->Instance->CR |= (uint32_t)(DCMI_Mode);

  /* Set the DMA memory0 conversion complete callback */
  hdcmi->DMA_Handle->XferCpltCallback = DCMI_DMAXferCplt;

  /* Set the DMA error callback */
  hdcmi->DMA_Handle->XferErrorCallback = DCMI_DMAError;

  /* Set the dma abort callback */
  hdcmi->DMA_Handle->XferAbortCallback = DCMI_Abort;

  /* Set the DMA memory1 conversion complete callback */
  hdcmi->DMA_Handle->XferM1CpltCallback = DCMI_DMAXferCplt;

  /* Initialize transfer parameters */
  hdcmi->XferCount = 100; // 480 lines
  hdcmi->XferSize = 320; // 320 words per line
  hdcmi->pBuffPtr = pData;

  /* Update DCMI counter  and transfer number*/
  hdcmi->XferCount = (hdcmi->XferCount - 2U);
  hdcmi->XferTransferNumber = hdcmi->XferCount;

  /* Update second memory address */
  SecondMemAddress = (uint32_t)(pData + (4U * hdcmi->XferSize));

  /* Start DMA multi buffer transfer */
  if (HAL_DMAEx_MultiBufferStart_IT(
          hdcmi->DMA_Handle, (uint32_t)&hdcmi->Instance->DR, (uint32_t)pData,
          SecondMemAddress, hdcmi->XferSize) != HAL_OK) {
    /* Set Error Code */
    hdcmi->ErrorCode = HAL_DCMI_ERROR_DMA;
    /* Change DCMI state */
    hdcmi->State = HAL_DCMI_STATE_READY;
    /* Release Lock */
    __HAL_UNLOCK(hdcmi);
    /* Return function status */
    return HAL_ERROR;
  }

  /* Enable Capture */
  hdcmi->Instance->CR |= DCMI_CR_CAPTURE;

  /* Release Lock */
  __HAL_UNLOCK(hdcmi);

  /* Return function status */
  return HAL_OK;
}
void camera_power_init(void) {
  GPIO_InitTypeDef gpio;
  CAMERA_POWER_GPIO_CLK_ENABLE();
  gpio.Pin = CAMERA_POWER_GPIO_PIN;
  gpio.Mode = GPIO_MODE_OUTPUT_PP;
  gpio.Pull = GPIO_PULLDOWN;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(CAMERA_POWER_GPIO_PORT, &gpio);
}

void camera_led_init(void) {
  GPIO_InitTypeDef gpio;
  gpio.Mode = GPIO_MODE_OUTPUT_PP;
  gpio.Pull = GPIO_PULLDOWN;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;

  if (PCB_V1_0 == device_get_pcb_version()) {
    CAMERA_LED_GPIO_CLK_ENABLE();
    gpio.Pin = CAMERA_LED_GPIO_PIN;
    HAL_GPIO_Init(CAMERA_LED_GPIO_PORT, &gpio);
  } else if(PCB_V1_1 == device_get_pcb_version()) {
    V11_CAMERA_LED_GPIO_CLK_ENABLE();
    gpio.Pin = V11_CAMERA_LED_GPIO_PIN;
    HAL_GPIO_Init(V11_CAMERA_LED_GPIO_PORT, &gpio);
  }
}


void convert_rgb565_to_grayscale(void) {
  uint8_t *p = (uint8_t *)FMC_SDRAM_IMAGE_BUFFER_ADDRESS;
  uint8_t *gray = quirc_begin(qr, NULL, NULL);
  for (int i = 0; i < window.width * window.height; i++) {
    uint16_t rgb565 = p[1] << 8 | p[0];
    uint8_t r = (rgb565 >> 11) & 0x1F;
    uint8_t g = (rgb565 >> 5) & 0x3F;
    uint8_t b = rgb565 & 0x1F;
    *gray++ = (r * 77 + g * 151 + b * 28) >> 8;
    p += 2;
  }
}

void histogram_equalization() {
    uint32_t histogram[256] = {0};
    uint32_t cdf[256] = {0};
    int count = window.width * window.height;
    uint8_t *gray = (uint8_t *)FMC_SDRAM_QUIRC_BUFFER_ADDRESS;

    // 1. 计算直方图
    for (int i = 0; i < count; i++) {
        histogram[gray[i]]++;
    }

    // 2. 计算累积分布函数 (CDF)
    cdf[0] = histogram[0];
    for (int i = 1; i < 256; i++) {
        cdf[i] = cdf[i - 1] + histogram[i];
    }

    // 3. 归一化 CDF
    int cdf_min = cdf[0];
    for (int i = 0; i < 256; i++) {
        cdf[i] = ((cdf[i] - cdf_min) * 255) / (count - cdf_min);
    }

    // 4. 映射像素值
    for (int i = 0; i < count; i++) {
        gray[i] = cdf[gray[i]];
    }
}

#if SENSOR_OUT_IMAGE_NEED_ROTATE
#define CLOCK_WISH 0
static void rotate_image(void) {
#if CLOCK_WISH
  // 1 2 3      7 4 1
  // 4 5 6  =>  8 5 2
  // 7 8 9      9 6 3

  // rgb565 ---- uint16_t
  uint16_t (*src)[400] = (uint16_t(*)[400])FMC_SDRAM_CAMERA_BUFFER_ADDRESS;
  uint16_t (*dst)[400] = (uint16_t(*)[400])FMC_SDRAM_IMAGE_BUFFER_ADDRESS;
  for (int i = 0; i < window.width; i++) {
    for (int j = 0; j < window.height; j++) {
      dst[j][400-i-1] = src[i][j];
    }
  }
#else
  // 1 2 3      3 6 9
  // 4 5 6  =>  2 5 8
  // 7 8 9      1 4 7

  // rgb565 ---- uint16_t
  uint16_t (*src)[400] = (uint16_t(*)[400])FMC_SDRAM_CAMERA_BUFFER_ADDRESS;
  uint16_t (*dst)[400] = (uint16_t(*)[400])FMC_SDRAM_IMAGE_BUFFER_ADDRESS;
  for (int i = 0; i < window.width; i++) {
    for (int j = 0; j < window.height; j++) {
      dst[400-j-1][i] = src[i][j];
    }
  }
#endif
}
#endif

#if CAMERA_SHOW_GRAY
static void gray_to_rgb565(void) {
  uint8_t *src = (uint8_t *)FMC_SDRAM_QUIRC_BUFFER_ADDRESS;
  uint16_t *dst = (uint16_t *)CAMERA_TEST_BUFFER;
  for (int i = 0; i < window.width * window.height; i++) {
    uint8_t gray = *src++;
    uint8_t r = (gray >> 3) & 0x1F;  // 5 bits for red
    uint8_t g = (gray >> 2) & 0x3F;  // 6 bits for green
    uint8_t b = (gray >> 3) & 0x1F;  // 5 bits for blue

    // Combine into RGB565 format
    uint16_t rgb565 = (r << 11) | (g << 5) | b;
    *dst++ = rgb565;
  }
}

static void gray2_to_rgb565(void) {
  uint8_t *src = (uint8_t *)FMC_SDRAM_QUIRC_BUFFER_ADDRESS;
  uint16_t *dst = (uint16_t *)CAMERA_TEST_BUFFER;
  for (int i = 0; i < window.width * window.height; i++) {
    // quirc 处理过之后的gray只有0和1
    uint16_t c = *src++ ? 0xFF : 0x00;
    *dst++ = c;
  }

}
#endif


int camera_scan_qrcode(uint8_t qrcode[1024 + 1], int *type) {
  if (qr_status != QR_GRAYSCALE) {
    return -1;
  }
  quirc_end_sliding(qr, 40);
  int count = quirc_count(qr);
  if (count == 0) {
    qr_status = QR_NONE;
    return -2;
  }
  printf("qr code count: %d\n", count);

  struct quirc_code code;
  struct quirc_data data;
  quirc_extract(qr, 0, &code);
  quirc_decode_error_t err = quirc_decode(&code, &data);
  if (err == QUIRC_ERROR_DATA_ECC) {
    quirc_flip(&code);
    err = quirc_decode(&code, &data);
  }

  qr_status = QR_CODE;
  if (err != QUIRC_SUCCESS) {
    printf("qr code decode failed: %s\n", quirc_strerror(err));
    return 0;
  }
  if (data.payload_len > 1024) {
    return -3;
  }
  *type = data.data_type;
  memcpy(qrcode, data.payload, data.payload_len);
  return data.payload_len;
}

// void DMA2D_IRQHandler(void) { HAL_DMA2D_IRQHandler(&hdma2d); }

/// dcmi callbacks
void HAL_DCMI_ErrorCallback(DCMI_HandleTypeDef *hdcmi) {
  if (hdcmi->ErrorCode == 0) {
    return;
  }
  camera_deinit();
}
void HAL_DCMI_FrameEventCallback(DCMI_HandleTypeDef *hdcmi) {
  // not used
  (void)hdcmi;
  camera_suspend();
#if SENSOR_OUT_IMAGE_NEED_ROTATE
  rotate_image();
#endif
  // no need convert gray while COVERING or already gray
  if (qr_status != QR_GRAYSCALE && qr_status != QR_MAKING_GRAYSCALE) {
    qr_status = QR_MAKING_GRAYSCALE;
    convert_rgb565_to_grayscale();
    // 增加对比度
    histogram_equalization();
    qr_status = QR_GRAYSCALE;
  }
#if CAMERA_SHOW_GRAY
  gray_to_rgb565();
  char value[1024+1] = {0};
  int type = 0;
  int len = camera_scan_qrcode((uint8_t*)value, &type);
  if (len > 0) {
    printf("camera scan qrcode: %s\n", value);
  } else {
    printf("camera scan qrcode failed: %d\n", len);
  }
  gray2_to_rgb565();
#endif
  camera_resume();
}

/// DCMI initialization
static void DCMI_MspInit(DCMI_HandleTypeDef *hdcmi) {
  static DMA_HandleTypeDef hdma_handler;
  GPIO_InitTypeDef gpio_init_structure;

  /*** Enable peripherals and GPIO clocks ***/
  /* Enable DCMI clock */
  __HAL_RCC_DCMI_CLK_ENABLE();

  /* Enable DMA2 clock */
  __HAL_RCC_DMA2_CLK_ENABLE();

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOG_CLK_ENABLE();

   // HSYNC PCLK  D0 D1
  gpio_init_structure.Pin       = GPIO_PIN_4 | GPIO_PIN_6 | GPIO_PIN_9 | GPIO_PIN_10;
  gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
  gpio_init_structure.Pull      = GPIO_PULLUP;
  gpio_init_structure.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio_init_structure.Alternate = GPIO_AF13_DCMI;
  HAL_GPIO_Init(GPIOA, &gpio_init_structure);

  // D5
  gpio_init_structure.Pin       = GPIO_PIN_3;
  gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
  gpio_init_structure.Pull      = GPIO_PULLUP;
  gpio_init_structure.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio_init_structure.Alternate = GPIO_AF13_DCMI;
  HAL_GPIO_Init(GPIOD, &gpio_init_structure);

  //  D4 D6 D7
  gpio_init_structure.Pin       = GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6;
  gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
  gpio_init_structure.Pull      = GPIO_PULLUP;
  gpio_init_structure.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio_init_structure.Alternate = GPIO_AF13_DCMI;
  HAL_GPIO_Init(GPIOE, &gpio_init_structure);

  // VSYNC D2 D3
  gpio_init_structure.Pin       = GPIO_PIN_9 | GPIO_PIN_10 | GPIO_PIN_11;
  gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
  gpio_init_structure.Pull      = GPIO_PULLUP;
  gpio_init_structure.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio_init_structure.Alternate = GPIO_AF13_DCMI;
  HAL_GPIO_Init(GPIOG, &gpio_init_structure);

  /*** Configure the DMA ***/
  /* Set the parameters to be configured */
  hdma_handler.Init.Request             = DMA_REQUEST_DCMI;
  hdma_handler.Init.Direction           = DMA_PERIPH_TO_MEMORY;
  hdma_handler.Init.PeriphInc           = DMA_PINC_DISABLE;
  hdma_handler.Init.MemInc              = DMA_MINC_ENABLE;
  hdma_handler.Init.PeriphDataAlignment = DMA_PDATAALIGN_WORD;
  hdma_handler.Init.MemDataAlignment    = DMA_MDATAALIGN_WORD;
  hdma_handler.Init.Mode                = DMA_CIRCULAR;
  hdma_handler.Init.Priority            = DMA_PRIORITY_HIGH;
  hdma_handler.Init.FIFOMode            = DMA_FIFOMODE_ENABLE;
  hdma_handler.Init.FIFOThreshold       = DMA_FIFO_THRESHOLD_FULL;
  hdma_handler.Init.MemBurst            = DMA_MBURST_SINGLE;
  hdma_handler.Init.PeriphBurst         = DMA_PBURST_SINGLE;
  hdma_handler.Instance                 = DMA2_Stream3;

  /* Associate the initialized DMA handle to the DCMI handle */
  __HAL_LINKDMA(hdcmi, DMA_Handle, hdma_handler);

  /*** Configure the NVIC for DCMI and DMA ***/
  /* NVIC configuration for DCMI transfer complete interrupt */
  HAL_NVIC_SetPriority(DCMI_IRQn, 8, 0);
  HAL_NVIC_EnableIRQ(DCMI_IRQn);

  /* NVIC configuration for DMA2D transfer complete interrupt */
  HAL_NVIC_SetPriority(DMA2_Stream3_IRQn, 9, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream3_IRQn);

  /* Configure the DMA stream */
  (void)HAL_DMA_Init(hdcmi->DMA_Handle);
}

HAL_StatusTypeDef MX_DCMI_Init(DCMI_HandleTypeDef* hdcmi)
{
  /*** Configures the DCMI to interface with the camera module ***/
  /* DCMI configuration */
  hdcmi->Instance              = DCMI;
  hdcmi->Init.CaptureRate      = DCMI_CR_ALL_FRAME;
  hdcmi->Init.HSPolarity       = DCMI_HSPOLARITY_HIGH;
  hdcmi->Init.SynchroMode      = DCMI_SYNCHRO_HARDWARE;
  hdcmi->Init.VSPolarity       = DCMI_VSPOLARITY_HIGH;
  hdcmi->Init.ExtendedDataMode = DCMI_EXTEND_DATA_8B;
  hdcmi->Init.PCKPolarity      = DCMI_PCKPOLARITY_RISING;

  if(HAL_DCMI_Init(hdcmi) != HAL_OK)
  {
    return HAL_ERROR;
  }
  return HAL_OK;
}

static void DCMI_MspDeInit(DCMI_HandleTypeDef *hdcmi)
{
  GPIO_InitTypeDef gpio_init_structure;

  /* Disable NVIC  for DCMI transfer complete interrupt */
  HAL_NVIC_DisableIRQ(DCMI_IRQn);

  /* Disable NVIC for DMA2 transfer complete interrupt */
  HAL_NVIC_DisableIRQ(DMA2_Stream3_IRQn);

  /* Configure the DMA stream */
  (void)HAL_DMA_DeInit(hdcmi->DMA_Handle);

  /* DeInit DCMI GPIOs */
  // HSYNC PCLK  D0 D1
  gpio_init_structure.Pin       = GPIO_PIN_4 | GPIO_PIN_6 | GPIO_PIN_9 | GPIO_PIN_10;
  HAL_GPIO_DeInit(GPIOA, gpio_init_structure.Pin);

  // D5
  gpio_init_structure.Pin       = GPIO_PIN_3;
  HAL_GPIO_DeInit(GPIOD, gpio_init_structure.Pin);

  // D4 D6 D7
  gpio_init_structure.Pin       = GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6;
  HAL_GPIO_DeInit(GPIOE, gpio_init_structure.Pin);

  // VSYNC D2 D3
  gpio_init_structure.Pin       = GPIO_PIN_3 | GPIO_PIN_10 | GPIO_PIN_11;
  HAL_GPIO_DeInit(GPIOG, gpio_init_structure.Pin);

  /* Disable DCMI clock */
  __HAL_RCC_DCMI_CLK_DISABLE();
}

/// DCMI IRQ
void DCMI_IRQHandler(void) {
  HAL_DCMI_IRQHandler(&hdcmi);
}

/// DCMI DMA IRQ
void DMA2_Stream3_IRQHandler(void) {
  HAL_DMA_IRQHandler(hdcmi.DMA_Handle);
}
