#include STM32_HAL_H

#include <stdbool.h>
#include "sys.h"
#include "device.h"
#include "power_manager.h"

void motor_init(void) {
  if (PCB_IS_V10()) {
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
}

void motor_ctrl(bool on) {
  if (PCB_IS_V10()) {
    if (on) {
      HAL_GPIO_WritePin(GPIOJ, GPIO_PIN_8, GPIO_PIN_SET);
    } else {
      HAL_GPIO_WritePin(GPIOJ, GPIO_PIN_8, GPIO_PIN_RESET);
    }
  } else if (PCB_IS_V11()){
    if (on) {
      pm_power_up(POWER_MODULE_MOTOR);
    } else {
      pm_power_down(POWER_MODULE_MOTOR);
    }
  }
}
