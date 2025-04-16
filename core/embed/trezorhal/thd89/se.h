#ifndef _SE_H_
#define _SE_H_

#include <stdint.h>
#include <stddef.h>

#define SE_POWER_ON() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_SET)
#define SE_POWER_OFF() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_RESET)

#if 0
// use PK5 as handshake pin
#define SE_COMBUS_GPIO_PORT GPIOK
#define SE_COMBUS_GPIO_PIN GPIO_PIN_5
#else
// use PB15 as handshake pin for testing
#define SE_COMBUS_GPIO_PORT GPIOB
#define SE_COMBUS_GPIO_PIN GPIO_PIN_15
#endif

#define SE_COMBUS_HIGH() HAL_GPIO_WritePin(SE_COMBUS_GPIO_PORT, SE_COMBUS_GPIO_PIN, GPIO_PIN_SET)
#define SE_COMBUS_LOW() HAL_GPIO_WritePin(SE_COMBUS_GPIO_PORT, SE_COMBUS_GPIO_PIN, GPIO_PIN_RESET)

#if !EMULATOR
int se_spi_init(void);
int se_send(uint8_t *buf, size_t size, uint32_t timeout);
int se_recv(uint8_t *buf, size_t size, uint32_t timeout);
#endif

#endif
