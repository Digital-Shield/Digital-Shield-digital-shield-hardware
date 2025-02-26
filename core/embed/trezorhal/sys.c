#include STM32_HAL_H

#include <stdbool.h>
#include "sys.h"

void motor_init(void) {
  GPIO_InitTypeDef gpio;

  __HAL_RCC_GPIOJ_CLK_ENABLE();

  // PK2, PK3
  gpio.Pin = GPIO_PIN_8;
  gpio.Mode = GPIO_MODE_OUTPUT_PP;
  gpio.Pull = GPIO_PULLDOWN;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;
  gpio.Alternate = 0;
  HAL_GPIO_Init(GPIOJ, &gpio);
}

void motor_ctrl(bool on) {
  if (on) {
    HAL_GPIO_WritePin(GPIOJ, GPIO_PIN_8, GPIO_PIN_SET);
  } else {
    HAL_GPIO_WritePin(GPIOJ, GPIO_PIN_8, GPIO_PIN_RESET);
  }
}
