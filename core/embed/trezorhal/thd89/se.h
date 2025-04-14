#ifndef _SE_H_
#define _SE_H_

#include <stdint.h>

#define SE_POWER_ON() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_SET)
#define SE_POWER_OFF() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_RESET)

// use GPIOK 5 as handshake pin
#define SE_COMBUS_HIGH() HAL_GPIO_WritePin(GPIOK, GPIO_PIN_5, GPIO_PIN_SET)
#define SE_COMBUS_LOW() HAL_GPIO_WritePin(GPIOK, GPIO_PIN_5, GPIO_PIN_RESET)

#if !EMULATOR
int32_t se_init_(void);
int32_t se_send(uint8_t *buf, uint32_t size);
int32_t se_recv(uint8_t *buf, uint32_t size);
#endif

#endif
