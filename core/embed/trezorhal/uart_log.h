#ifndef __TREZORHAL_UART_LOG_H__
#define __TREZORHAL_UART_LOG_H__

#include STM32_HAL_H

#if UART_LOG
int uart_log_init(void);
#else
#define uart_log_init()
#endif
#endif

#
