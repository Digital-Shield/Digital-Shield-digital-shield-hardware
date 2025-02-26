#ifndef __I2C_H__
#define __I2C_H__
#include STM32_HAL_H

#include "stm32h7xx_hal_i2c.h"

/**
 * I2C4
 * PIN:
 *    SCL: PD12
 *    SDA: PD13
 */

#define I2C4_CLK_ENABLE() __HAL_RCC_I2C4_CLK_ENABLE()
#define I2C4_FORCE_RESET() __HAL_RCC_I2C4_FORCE_RESET()
#define I2C4_RELEASE_RESET() __HAL_RCC_I2C4_RELEASE_RESET()
#define I2C4_PORT_CLK_ENABLE() __HAL_RCC_GPIOD_CLK_ENABLE()

#define I2C4_PORT GPIOD
#define I2C4_SCL_PIN GPIO_PIN_12
#define I2C4_SDA_PIN GPIO_PIN_13

#define I2C_TIMEOUT 1000

extern I2C_HandleTypeDef hi2c4;

void i2c4_init(void);
// try lock i2c4, return 0 if lock success, else return 1
int i2c4_try_lock(void);
// lock i2c4, wait until lock success
void i2c4_lock(void);
// unlock i2c4
void i2c4_unlock(void);

#define i2c4_write_reg(addr, reg, data, len) HAL_I2C_Mem_Write(&hi2c4, addr, reg, I2C_MEMADD_SIZE_8BIT, data, len, I2C_TIMEOUT)
#define i2c4_write_reg16(addr, reg, data, len) HAL_I2C_Mem_Write(&hi2c4, addr, reg, I2C_MEMADD_SIZE_16BIT, data, len, I2C_TIMEOUT)
#define i2c4_read_reg(addr, reg, data, len) HAL_I2C_Mem_Read(&hi2c4, addr, reg, I2C_MEMADD_SIZE_8BIT, data, len, I2C_TIMEOUT)
#define i2c4_read_reg16(addr, reg, data, len) HAL_I2C_Mem_Read(&hi2c4, addr, reg, I2C_MEMADD_SIZE_16BIT, data, len, I2C_TIMEOUT)

#endif
