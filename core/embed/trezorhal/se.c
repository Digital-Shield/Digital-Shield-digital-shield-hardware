#include STM32_HAL_H
#include <stdio.h>
#include <string.h>
#include "common.h"
#include "se.h"

static SPI_HandleTypeDef hspi5 = {0};
#define SE_TRANS_TIMEOUT 10000

int32_t se_init_(void) {
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /**SPI5 GPIO Configuration
  PK0     ------> SPI5_SCK
  PK1     ------> SPI5_NSS  --> se_cs
  PF8     ------> SPI5_MISO
  PJ10     ------> SPI5_MOSI
  */
  __HAL_RCC_SPI5_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOK_CLK_ENABLE();
  __HAL_RCC_GPIOJ_CLK_ENABLE();

  GPIO_InitStruct.Pin = GPIO_PIN_8;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF5_SPI5;
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

  GPIO_InitStruct.Pin = GPIO_PIN_0|GPIO_PIN_1;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF5_SPI5;
  HAL_GPIO_Init(GPIOK, &GPIO_InitStruct);

  GPIO_InitStruct.Pin = GPIO_PIN_10;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF5_SPI5;
  HAL_GPIO_Init(GPIOJ, &GPIO_InitStruct);

  // GPIO_InitStruct.Pin = GPIO_PIN_11;
  // GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  // GPIO_InitStruct.Pull = GPIO_NOPULL;
  // GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  // GPIO_InitStruct.Alternate = GPIO_AF5_SPI5;
  // HAL_GPIO_Init(GPIOJ, &GPIO_InitStruct);

  // power on
  GPIO_InitStruct.Pin = GPIO_PIN_4;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  // se hand
  GPIO_InitStruct.Pin = GPIO_PIN_5;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(GPIOK, &GPIO_InitStruct);

  // se power off
  // SE_POWER_OFF();
  // se power on
  SE_POWER_ON();

  /* SPI5 parameter configuration*/
  hspi5.Instance = SPI5;
  hspi5.Init.Mode = SPI_MODE_MASTER;
  hspi5.Init.Direction = SPI_DIRECTION_2LINES;
  hspi5.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi5.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi5.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi5.Init.NSS = SPI_NSS_HARD_OUTPUT;
  hspi5.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_128;
  hspi5.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi5.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi5.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi5.Init.CRCPolynomial = 10;
  hspi5.Init.NSSPMode = SPI_NSS_PULSE_ENABLE;
  hspi5.Init.NSSPolarity = SPI_NSS_POLARITY_LOW;
  hspi5.Init.FifoThreshold = SPI_FIFO_THRESHOLD_01DATA;
  hspi5.Init.TxCRCInitializationPattern = SPI_CRC_INITIALIZATION_ALL_ZERO_PATTERN;
  hspi5.Init.RxCRCInitializationPattern = SPI_CRC_INITIALIZATION_ALL_ZERO_PATTERN;
  hspi5.Init.MasterSSIdleness = SPI_MASTER_SS_IDLENESS_00CYCLE;
  hspi5.Init.MasterInterDataIdleness = SPI_MASTER_INTERDATA_IDLENESS_00CYCLE;
  hspi5.Init.MasterReceiverAutoSusp = SPI_MASTER_RX_AUTOSUSP_DISABLE;
  hspi5.Init.MasterKeepIOState = SPI_MASTER_KEEP_IO_STATE_DISABLE;
  hspi5.Init.IOSwap = SPI_IO_SWAP_DISABLE;

  HAL_SPI_DeInit(&hspi5);
  
  if (HAL_SPI_Init(&hspi5) != HAL_OK)
  {
    return -1;
  }
  
  return 0;
}

int32_t se_send(uint8_t *buf, uint32_t size) {
  if (HAL_SPI_Transmit(&hspi5, buf, size, SE_TRANS_TIMEOUT) != HAL_OK) {
    return -1; 
  }
  return 0;
}

int32_t se_recv(uint8_t *buf, uint32_t size) {
  if (HAL_SPI_Receive(&hspi5, buf, size, SE_TRANS_TIMEOUT) != HAL_OK) {
    return -1; 
  }
  return 0;
}
uint8_t se_test(void) {
	uint8_t send[512] = {0xAA, 0x00, 0x05, 0x00, 0x84, 0x00, 0x00, 0x08, 0x8C};
	uint8_t tag, recv[512] = {0};
	// uint8_t lc[2];

	HAL_Delay(100);
	// for(uint8_t i = 0; i < 0xff; i++) {
	// 	send[2+i] = i;
	// }
	// send[0] = 0xaa;
	// send[1] = 0x40;
	// HAL_GPIO_WritePin(GPIOK, GPIO_PIN_1, GPIO_PIN_RESET); // hard control CS
	// se_send(send, 0x40 + 2);
	se_send(send, 9);
	// HAL_GPIO_TogglePin(GPIOK, GPIO_PIN_1); // hard control CS

	// wait slave processed
	HAL_Delay(100);
	// wait handshake single
	// while(HAL_GPIO_ReadPin(GPIOJ, GPIO_PIN_5) != GPIO_PIN_RESET);

	// thd89-process-loop...
	// se_recv(&tag, 1);
	// //if (tag != 0xaa) return 0;
	// se_recv(lc, 2);
	// lc = 0x40;
	// se_recv(recv, lc);
  (void)tag;
	se_recv(recv, 14);
	HAL_Delay(100);
	// if (memcmp(recv, send, lc) != 0) return 0;

	return 1;
	//HAL_GPIO_WritePin(GPIOK, GPIO_PIN_1, GPIO_PIN_SET);
	//HAL_GPIO_WritePin(GPIOJ, GPIO_PIN_5, GPIO_PIN_SET); // stop send
}

void test_miso(void) {
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  __HAL_RCC_GPIOF_CLK_ENABLE();

  GPIO_InitStruct.Pin = GPIO_PIN_8;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_8, GPIO_PIN_SET);
  while(1) {
    HAL_Delay(100);
    HAL_GPIO_TogglePin(GPIOF, GPIO_PIN_8);
  }
}