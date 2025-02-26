#include STM32_HAL_H
#include "battery.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static I2C_HandleTypeDef hi2c1 = {0};
#define I2C_TRANSMIT_TIMEOUT 10000

/* I2C TIMING Register define when I2C clock source is HSI*/
/* I2C TIMING is calculated in case of the I2C Clock source is the HSI = 16 MHz */
/* This example use TIMING to 0x0020098E to reach 400Khz speed (Rise time = 50ns, Fall time = 10ns) */
#define I2C_TIMING             0x70B03140 // 0x70B03140 0x00200817
#define RT9426_ADDR            0x55 << 1
#define MASK_REG_FLAG3_BSC_ACS 0x01
#define SWVER                  0x01

#define REG_CNTL               (0x00)
#define REG_RSVD               (0x02)
#define REG_CURR               (0x04)
#define REG_TEMP               (0x06)
#define REG_VBAT               (0x08)
#define REG_FLAG1              (0x0A)
#define REG_FLAG2              (0x0C)
#define REG_RM                 (0x10)
#define REG_FCC                (0x12)
#define REG_AC                 (0x14)
#define REG_TTE                (0x16)
#define REG_DUMMY              (0x1E) // Add Dummy Write by V1.1.0
#define REG_INTT               (0x28)
#define REG_CYC                (0x2A)
#define REG_SOC                (0x2C)
#define REG_SOH                (0x2E)
#define REG_VER                (0x20)
#define REG_FLAG3              (0x30)
#define REG_IRQ                (0x36)
#define REG_DC                 (0x3C)
#define REG_BDCNTL             (0x3E)
#define REG_CMD3F              (0x3F)
#define REG_SWINDOW1           (0x40)
#define REG_SWINDOW2           (0x42)
#define REG_SWINDOW3           (0x44)
#define REG_SWINDOW4           (0x46)
#define REG_SWINDOW5           (0x48)
#define REG_SWINDOW6           (0x4A)
#define REG_SWINDOW7           (0x4C)
#define REG_SWINDOW8           (0x4E)
#define REG_CMD60              (0x60)
#define REG_CMD61              (0x61)
#define REG_CMD78              (0x78)

#define OP_CHECK(r)     \
    do                  \
    {                   \
        if ( (r) != 0 ) \
        {               \
            return -1;  \
        }               \
    }                   \
    while ( 0 )

#define delay(x) HAL_Delay(x)
int i2c_master_write(uint8_t addr, uint8_t* buf, uint8_t len)
{
    if ( HAL_I2C_Master_Transmit(&hi2c1, addr, (uint8_t*)buf, len, I2C_TRANSMIT_TIMEOUT) != HAL_OK )
    {
        return -1;
    }

    return 0;
}
int i2c_master_read(uint8_t addr, uint8_t* buf, uint8_t len)
{
    if ( HAL_I2C_Master_Receive(&hi2c1, addr, (uint8_t*)buf, len, I2C_TRANSMIT_TIMEOUT) != HAL_OK )
    {
        return -1;
    }
    return 0;
}
int battery_write_register(uint8_t Reg_Addr, uint16_t data)
{
    uint8_t buffer[8] = {0};

    buffer[0] = Reg_Addr;
    buffer[1] = (unsigned char)data;
    buffer[2] = (unsigned char)(data >> 8);
    return i2c_master_write(RT9426_ADDR, buffer, 3);
}

int battery_read_register(uint8_t Reg_Addr, int16_t* data)
{
    uint8_t buf[8] = {0};
    int result;

    buf[0] = Reg_Addr;
    result = i2c_master_write(RT9426_ADDR, buf, 1);
    OP_CHECK(result);
    result = i2c_master_read(RT9426_ADDR, buf, 2);
    OP_CHECK(result);
    *data = buf[1] << 8 | buf[0];
    return 0;
}

int battery_read_current(void)
{
    int result = 0;
    int16_t ret;
    result = battery_read_register(REG_CURR, &ret);
    OP_CHECK(result);
    return ret;
}

int battery_read_voltage(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_VBAT, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_temperature(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_TEMP, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_remained_capacity(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_RM, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_full_capacity(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_FCC, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_average_current(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_AC, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_SOC(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_SOC, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_SOH(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_SOH, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_design_capacity(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_DC, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_time_to_empty(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_TTE, &ret);
    OP_CHECK(result);

    return ret;
}

int battery_read_state_of_health(void)
{
    int result = 0;
    int16_t ret;

    result = battery_read_register(REG_SOH, &ret);
    OP_CHECK(result);

    return ret;
}

int RT9426_Initial(void)
{
/*---------------Define RT9426 Initail Setting----------------------*/
#define RT9426_CFG_VERSION  (0x01)
#define RT9426_BATTERY_TYPE (620)
#define RT9426_DC           (620)
#define RT9426_FCC          (620)
#define RT9426_FC_VTH       (0x71)
#define RT9426_FC_ITH       (0x1F)
#define RT9426_FC_STH       (0x46)
#define RT9426_FD_VTH       (0xB2)
#define RT9426_OPCFG1       (0x3480)
#define RT9426_OPCFG2       (0x0000)
#define RT9426_OPCFG3       (0x3CFF)
#define RT9426_OPCFG4       (0x2000)
#define RT9426_OPCFG5       (0x0C7F)
#define RT9426_OTC_TTH      (0x0064)
#define RT9426_OTC_CHG_ITH  (0x0B5F)
#define RT9426_OTD_TTH      (0x0064)
#define RT9426_OTD_DCHG_ITH (0x0B5F)
#define RT9426_UVOV_TH      (0x00FF)
#define RT9426_US_TH        (0x00)
#define RT9426_CURR_DB      (0x05)
#define RT9426_QS_EN        (0x01)

    const uint32_t g_basic_key = 0x12345678;
    // uint32_t g_advance_key = 0xFFFFFFFF;
    // uint16_t RT9426_EXTREG_SIZE = 25;
    // uint16_t RT9426_EXTREG_DATA[75] = {
    //     0x0, 0x42, 0x7749, 0x0, 0x44, 0xB7A4, 0x0, 0x48, 0x85A7, 0x0, 0x4A, 0x4160, 0x5, 0x4E, 0x000A,
    //     0x6, 0x48, 0x332A, 0x6, 0x4A, 0x6852, 0x6, 0x4C, 0x6457, 0x6, 0x4E, 0x1760, 0x7, 0x40, 0x5A99,
    //     0x7, 0x42, 0x2E1A, 0x7, 0x44, 0x2E2E, 0x7, 0x46, 0x2121, 0x7, 0x48, 0x9EDF, 0x7, 0x4A, 0x232B,
    //     0x7, 0x4C, 0x1923, 0x7, 0x4E, 0xD919, 0x8, 0x40, 0xFE99, 0x8, 0x42, 0x1414, 0x8, 0x44, 0xEFEF,
    //     0x8, 0x46, 0x81B0, 0x8, 0x48, 0x14FE, 0x8, 0x4A, 0xEF14, 0x8, 0x4C, 0xB0EF, 0x8, 0x4E, 0x0081
    // };

    uint16_t RT9426_USR_OCV_TABLE[80] = {
        0x0013, 0x49C0, 0x5480, 0x5526, 0x55B3, 0x5660, 0x5806, 0x59AD, 0x5ABA, 0x5B8D, 0x5C7A, 0x5D40,
        0x5DF3, 0x5FFA, 0x61B3, 0x630D, 0x6413, 0x65C6, 0x6800, 0x706D, 0x2B00, 0x00A6, 0x006C, 0x00B6,
        0x006C, 0x0058, 0x0021, 0x0032, 0x0058, 0x006B, 0x0066, 0x0067, 0x006C, 0x008D, 0x007D, 0x00C1,
        0x00A5, 0x035F, 0x0013, 0xFF80, 0x0000, 0x0200, 0x049A, 0x0680, 0x0E4D, 0x17E6, 0x281A, 0x309A,
        0x3600, 0x39B3, 0x3D33, 0x474D, 0x4F80, 0x5466, 0x589A, 0x5D1A, 0x6400, 0x6900, 0x0006, 0x018A,
        0x025D, 0x0168, 0x025D, 0x02E9, 0x07B7, 0x0527, 0x02EB, 0x0263, 0x0280, 0x027E, 0x0260, 0x01D1,
        0x020C, 0x0153, 0x018D, 0x004C, 0x2EB7, 0x0000, 0x0000, 0x0000
    };

    uint8_t /*loop = 0,*/ retry_times = 0;
    uint8_t i, j;
    int16_t regval = 0;
    int16_t sts = 0;
    uint8_t count = 0;

    /*------------------------Unseal RT9426----------------------------*/
    while ( 1 )
    {
        count++;
        if ( battery_write_register(REG_CNTL, g_basic_key & 0xFFFF) == 0 )
        {
            delay(1);
            if ( battery_write_register(REG_CNTL, g_basic_key >> 16) == 0 )
            {
                battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
                delay(1);

                battery_read_register(REG_FLAG3, &sts);
                if ( sts & MASK_REG_FLAG3_BSC_ACS )
                {
                    break;
                }
            }
        }
        if ( count > 5 )
        {
            return -1;
        }
        delay(10);
    }
    /*------------------------Unseal RT9426----------------------------*/

    /*---------------------Set User Define OCV Table--------------------------*/
    if ( RT9426_USR_OCV_TABLE[0] == 0x0013 )
    {
        retry_times = 3;
        while ( retry_times )
        {
            for ( i = 0; i < 9; i++ )
            {
                battery_write_register(REG_BDCNTL, 0xCB00 + i);
                battery_write_register(REG_BDCNTL, 0xCB00 + i); // Add Page Dummy Write by V1.1.0
                delay(1);
                for ( j = 0; j < 8; j++ )
                {
                    battery_write_register(0x40 + j * 2, RT9426_USR_OCV_TABLE[i * 8 + j]);
                    delay(1);
                }
            }

            battery_write_register(REG_BDCNTL, 0xCB09);
            battery_write_register(REG_BDCNTL, 0xCB09); // Add Page Dummy Write by V1.1.0
            delay(1);
            for ( i = 0; i < 5; i++ )
            {
                battery_write_register(0x40 + i * 2, RT9426_USR_OCV_TABLE[72 + i]);
                delay(1);
            }
            battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
            delay(10);
            battery_read_register(REG_FLAG2, &regval);
            if ( regval & 0x0800 )
            {
                break;
            }

            retry_times--;

            if ( retry_times == 0 )
            {
                return -1;
            }
        }
    }
    /*---------------------Set User Define OCV Table--------------------------*/

    /*---------------Read Reg IRQ to reinital Alert pin state------------------*/
    battery_read_register(REG_IRQ, &regval);
    /*---------------Read Reg IRQ to reinital Alert pin state------------------*/

    /*------------------------Set Alert Threshold----------------------------*/
    battery_write_register(REG_BDCNTL, 0x6553);
    battery_write_register(REG_BDCNTL, 0x6553); // Add Page Dummy Write by V1.1.0
    delay(1);
    battery_write_register(REG_SWINDOW1, RT9426_OTC_TTH);
    delay(1);
    battery_write_register(REG_SWINDOW2, RT9426_OTC_CHG_ITH);
    delay(1);
    battery_write_register(REG_SWINDOW3, RT9426_OTD_TTH);
    delay(1);
    battery_write_register(REG_SWINDOW4, RT9426_OTD_DCHG_ITH);
    delay(1);
    battery_write_register(REG_SWINDOW5, RT9426_UVOV_TH);
    delay(1);
    battery_write_register(REG_SWINDOW6, ((0x4600) | (RT9426_US_TH)));
    // battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*------------------------Set Alert Threshold----------------------------*/

    /*-----------------------Set Default OCV Table---------------------------*/
    battery_write_register(REG_BDCNTL, 0x6552);
    battery_write_register(REG_BDCNTL, 0x6552); // Add Page Dummy Write by V1.1.0
    delay(1);
    battery_write_register(REG_SWINDOW1, 0x8000);
    // battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*-----------------------Set Default OCV Table---------------------------*/

    /*-------------------------Set OP CONFIG------------------------------*/
    // battery_write_register(REG_BDCNTL, 0x6551);
    // battery_write_register(REG_BDCNTL, 0x6551); // Add Page Dummy Write by V1.1.0
    // delay(1);
    battery_write_register(REG_SWINDOW1, RT9426_OPCFG1);
    delay(1);
    battery_write_register(REG_SWINDOW2, RT9426_OPCFG2);
    delay(1);
    battery_write_register(REG_SWINDOW3, RT9426_OPCFG3);
    delay(1);
    battery_write_register(REG_SWINDOW4, RT9426_OPCFG4);
    delay(1);
    battery_write_register(REG_SWINDOW5, RT9426_OPCFG5);
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*-------------------------Set OP CONFIG------------------------------*/

    /*----------------------Set Current Deadband----------------------------*/
    battery_write_register(REG_BDCNTL, 0x6551);
    battery_write_register(REG_BDCNTL, 0x6551); // Add Page Dummy Write by V1.1.0
    delay(1);
    battery_write_register(REG_SWINDOW7, ((0x0012) | (RT9426_CURR_DB << 8)));
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*----------------------Set Current Deadband----------------------------*/

    /*-----------------------Set FC FD Threshold-----------------------------*/
    regval = (RT9426_FC_VTH) | (RT9426_FC_ITH << 8);
    battery_write_register(REG_BDCNTL, 0x6555);
    battery_write_register(REG_BDCNTL, 0x6555); // Add Page Dummy Write by V1.1.0
    delay(1);
    battery_write_register(REG_SWINDOW3, regval);
    delay(1);
    battery_write_register(REG_SWINDOW4, (0x4100 | RT9426_FC_STH));
    delay(1);
    battery_write_register(REG_SWINDOW6, (0x1200 | RT9426_FD_VTH));
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*-----------------------Set FC FD Threshold-----------------------------*/

    /*--------------------------Set DC & FCC-------------------------------*/
    battery_write_register(REG_BDCNTL, 0x6552);
    battery_write_register(REG_BDCNTL, 0x6552); // Add Page Dummy Write by V1.1.0
    delay(1);
    battery_write_register(REG_SWINDOW6, RT9426_DC);
    delay(1);
    battery_write_register(REG_SWINDOW7, RT9426_FCC);
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);

    /*--------------------------Set DC & FCC-------------------------------*/

    /*--------------------------Set Ext Register-----------------------------*/
    // if ( RT9426_EXTREG_SIZE != 0 )
    // {
    //     for ( loop = 0; loop < RT9426_EXTREG_SIZE; loop++ )
    //     {
    //         battery_write_register(REG_BDCNTL, 0x6550 + (RT9426_EXTREG_DATA[loop * 3]));
    //         battery_write_register(
    //             REG_BDCNTL, 0x6550 + (RT9426_EXTREG_DATA[loop * 3])
    //         ); // Add Page Dummy Write by V1.1.0
    //         delay(1);
    //         battery_write_register(RT9426_EXTREG_DATA[(loop * 3) + 1], RT9426_EXTREG_DATA[(loop * 3) + 2]);
    //         delay(1);
    //     }
    //     battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    // }
    /*--------------------------Set Ext Register-----------------------------*/

    /*---------------------------Quick Start--------------------------------*/
    if ( RT9426_QS_EN == 1 )
    {
        battery_write_register(REG_CNTL, 0x4000);
        battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
        delay(5);
    }
    /*---------------------------Quick Start--------------------------------*/

    /*-----------------------------Clear RI--------------------------------*/
    battery_read_register(REG_FLAG3, &regval);
    regval = (regval & ~0x0100);
    battery_write_register(REG_FLAG3, regval);
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(1);
    /*-----------------------------Clear RI--------------------------------*/

    /*------------------------Seal RT9426----------------------------*/
    battery_write_register(REG_CNTL, 0x0020);
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(5);                                  // RT0720 extend delay time

    /*------------------------Seal RT9426----------------------------*/
    return 0;
}

int battery_i2c_master_init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;

    __HAL_RCC_GPIOB_CLK_ENABLE();
    GPIO_InitStructure.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_LOW;
    GPIO_InitStructure.Alternate = GPIO_AF4_I2C1;
    GPIO_InitStructure.Pin = BATTERY_I2C_SCL_PIN | BATTERY_I2C_SDA_PIN;
    HAL_GPIO_Init(BATTERY_I2C_PORT, &GPIO_InitStructure);

    __HAL_RCC_I2C1_CLK_ENABLE();
    __HAL_RCC_I2C1_FORCE_RESET();
    __HAL_RCC_I2C1_RELEASE_RESET();

    hi2c1.Instance = I2C1;
    hi2c1.Init.Timing = I2C_TIMING;
    hi2c1.Init.OwnAddress1 = 0; // master
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.OwnAddress2 = 0;
    hi2c1.Init.OwnAddress2Masks = I2C_OA2_NOMASK;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_ENABLE;

    if ( HAL_OK != HAL_I2C_Init(&hi2c1) )
    {
        return -1;
    }

    /** Configure Analogue filter
     */
    if ( HAL_I2CEx_ConfigAnalogFilter(&hi2c1, I2C_ANALOGFILTER_ENABLE) != HAL_OK )
    {
        return -1;
    }
    /** Configure Digital filter
     */
    if ( HAL_I2CEx_ConfigDigitalFilter(&hi2c1, 0) != HAL_OK )
    {
        return -1;
    }
    return 0;
}

void battery_i2c_deinit(void)
{
    if ( hi2c1.Instance )
    {
        HAL_I2C_DeInit(&hi2c1);
        hi2c1.Instance = NULL;
    }
}
int battery_init(void)
{
    int result = 0;
    uint16_t count = 0;
    int16_t regval = 0;

    result = battery_i2c_master_init();
    OP_CHECK(result);
    /*-----------------------Standard initial-----------------------*/
    while ( 1 )
    {
        count++;
        battery_read_register(REG_FLAG2, &regval); //--check RDY
        if ( regval & 0x0080 )
        {

            /*-------------V1.1.0 Battery Present Check & Delay---------*/
            /*-----------------check Bat Present Flag------------------*/
            delay(5);
            battery_read_register(REG_FLAG2, &regval);
            if ( regval & 0x0040 ) //--check bat present
            {
                delay(55);
            }
            /*-----------------check Bat Present Flag------------------*/
            /*-------------V1.1.0 Battery Present Check & Delay---------*/

            battery_read_register(
                REG_FLAG3, &regval
            ); //--check RI  //Fixed the bug for read RI timing by V1.1.1
            if ( regval & 0x0100 )
            {
                RT9426_Initial();
                battery_write_register(REG_RSVD, SWVER);   //--record present SW version
                battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
                delay(5);                                  // RT0720 extend delay time
                break;
            }
            else
            {
                break;
            }
        }
        if ( count > 20 )
        {
            return -1;
        }
        delay(20);
    }
    /*-----------------------Standard initial-----------------------*/
    count = 0;

    /*---------V1.1.0 Force re-initial RT9426 when SW update---------*/
    /*------------------------Force initial--------------------------*/
    battery_read_register(REG_RSVD, &regval);
    if ( regval != SWVER )
    {
        /*-----------------check Bat Present Flag------------------*/
        RT9426_Initial();
        battery_write_register(REG_RSVD, SWVER);   //--record present SW version
        battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
        delay(5);                                  // Add delay by V1.1.2
        #if 0

        /* Reset IC for needed  */
        // Gauge_Write_Register(REG_CNTL,0x0041); //---reset RT9426
        // Delay_msecond(DELAY_1000MS);
        /* Reset IC for needed  */
        while ( 1 )
        {
            count++;
            battery_read_register(REG_FLAG2, &regval); //--check RDY
            if ( regval & 0x0080 )
            {
                /*-----------------check Bat Present Flag------------------*/
                delay(5);
                battery_read_register(REG_FLAG2, &regval);
                if ( regval & 0x0040 ) //--check bat present
                {
                    delay(55);
                }
                /*-----------------check Bat Present Flag------------------*/
                RT9426_Initial();
                battery_write_register(REG_RSVD, SWVER);   //--record present SW version
                battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
                delay(5);                                  // Add delay by V1.1.2
                break;
            }
            if ( count > 20 )
            {
                return -1;
            }
            delay(20);
        }
        #endif
    }
    /*------------------------Force initial-------------------------*/
    /*---------V1.1.0 Force re-initial RT9426 when SW update--------*/
    /*

    // test change battery 
    RT9426_Initial();
    battery_write_register(REG_RSVD, SWVER);   //--record present SW version
    battery_write_register(REG_DUMMY, 0x0000); // Add Dummy Write by V1.1.0
    delay(5);                                  // Add delay by V1.1.2
    */

    return 0;
}

void battery_test(void)
{
    int16_t bERR;
    static int16_t count;
    int result;
    short int ret;
    count++;
    printf("--------------------- %d", count);
    printf("--------------------- \n");
    bERR = battery_read_current();
    printf("电流 = %d mA\n", bERR);
    bERR = battery_read_voltage();
    printf("电压 = %d mV\n", bERR);
    bERR = battery_read_temperature();
    printf("温度 = %d\n", bERR);
    bERR = battery_read_remained_capacity();
    printf("剩余电量 = %d mAh\n", bERR);
    bERR = battery_read_full_capacity();
    printf("满电电量 = %d mAh\n", bERR);
    bERR = battery_read_average_current();
    printf("平均电流 = %d mA\n", bERR);
    bERR = battery_read_SOC();
    printf("电量 = %d%%\n", bERR);
    bERR = battery_read_design_capacity();
    printf("设计电量 = %d mAh\n", bERR);
    bERR = battery_read_time_to_empty();
    printf("可用时间 = %d M\n ", bERR);

    bERR = battery_read_state_of_health();
    printf("电池健康 = %d%%\n ", bERR);
    printf("--------------------------------------------------\n ");

    result = battery_read_register(REG_CNTL, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CNTL___\n ");
    }
    printf("REG_CNTL= %d \n", ret);

    result = battery_read_register(REG_RSVD, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_RSVD___\n ");
    }
    printf("REG_RSVD= %d \n", ret);
    result = battery_read_register(REG_CURR, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CURR___\n ");
    }
    printf("REG_CURR= %d \n", ret);
    result = battery_read_register(REG_TEMP, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_TEMP___\n ");
    }
    printf("REG_TEMP= %d \n", ret);

    result = battery_read_register(REG_VBAT, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_VBAT___\n ");
    }
    printf("REG_VBAT= %d \n", ret);

    result = battery_read_register(REG_FLAG1, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_FLAG1___\n ");
    }
    printf("REG_FLAG1= %d \n", ret);

    result = battery_read_register(REG_FLAG2, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_FLAG2___\n ");
    }
    printf("REG_FLAG2= %d \n", ret);

    result = battery_read_register(REG_RM, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_RM___\n ");
    }
    printf("REG_RM= %d \n", ret);

    result = battery_read_register(REG_FCC, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_FCC___\n ");
    }
    printf("REG_FCC= %d \n", ret);

    result = battery_read_register(REG_AC, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_AC___\n ");
    }
    printf("REG_AC= %d \n", ret);

    result = battery_read_register(REG_TTE, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_TTE___\n ");
    }
    printf("REG_TTE= %d \n", ret);

    result = battery_read_register(REG_DUMMY, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_DUMMY___\n ");
    }
    printf("REG_DUMMY= %d \n", ret);

    result = battery_read_register(REG_INTT, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_INTT___\n ");
    }
    printf("REG_INTT= %d \n", ret);

    result = battery_read_register(REG_CYC, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CYC___\n ");
    }
    printf("REG_CYC= %d \n", ret);

    result = battery_read_register(REG_SOC, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SOC___\n ");
    }
    printf("REG_SOC= %d \n", ret);

    result = battery_read_register(REG_SOH, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SOH___\n ");
    }
    printf("REG_SOH= %d \n", ret);

    result = battery_read_register(REG_VER, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_VER___\n ");
    }
    printf("REG_VER= %d \n", ret);

    result = battery_read_register(REG_FLAG3, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_FLAG3___\n ");
    }
    printf("REG_FLAG3= %d \n", ret);

    result = battery_read_register(REG_IRQ, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_IRQ___\n ");
    }
    printf("REG_IRQ= %d \n", ret);

    result = battery_read_register(REG_DC, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_DC___\n ");
    }
    printf("REG_DC= %d \n", ret);

    result = battery_read_register(REG_BDCNTL, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_BDCNTL___\n ");
    }
    printf("REG_BDCNTL= %d \n", ret);

    result = battery_read_register(REG_CMD3F, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CMD3F___\n ");
    }
    printf("REG_CMD3F= %d \n", ret);

    result = battery_read_register(REG_SWINDOW1, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW1___\n ");
    }
    printf("REG_SWINDOW1= %d \n", ret);

    result = battery_read_register(REG_SWINDOW2, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW2___\n ");
    }
    printf("REG_SWINDOW2= %d \n", ret);

    result = battery_read_register(REG_SWINDOW3, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW3___\n ");
    }
    printf("REG_SWINDOW3= %d \n", ret);

    result = battery_read_register(REG_SWINDOW4, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW4___\n ");
    }
    printf("REG_SWINDOW4= %d \n", ret);

    result = battery_read_register(REG_SWINDOW5, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW5___\n ");
    }
    printf("REG_SWINDOW5= %d \n", ret);

    result = battery_read_register(REG_SWINDOW6, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW6___\n ");
    }
    printf("REG_SWINDOW6= %d \n", ret);

    result = battery_read_register(REG_SWINDOW7, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW7___\n ");
    }
    printf("REG_SWINDOW7= %d \n", ret);

    result = battery_read_register(REG_SWINDOW8, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_SWINDOW8___\n ");
    }
    printf("REG_SWINDOW8= %d \n", ret);

    result = battery_read_register(REG_CMD60, &ret);
    if ( result != 0 )
    {
        printf("__ERR_RREG_CMD60___\n ");
    }
    printf("REG_CMD60= %d \n", ret);

    result = battery_read_register(REG_CMD61, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CMD61___\n ");
    }
    printf("REG_CMD61= %d \n", ret);

    result = battery_read_register(REG_CMD78, &ret);
    if ( result != 0 )
    {
        printf("__ERR_REG_CMD61___\n ");
    }
    printf("REG_CMD61= %d \n", ret);

    printf("--------------------------------------------------\n ");
}
