/*
 * This file is part of the Trezor project, https://trezor.io/
 *
 * Copyright (c) SatoshiLabs
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include STM32_HAL_H
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "common.h"
#include "i2c.h"
#include "secbool.h"

#include "display.h"
#include "touch.h"

/// CHSC6540
// address
#define TOUCH_ADDRESS (0x2EU << 1)

// registers
#define TOUCH_CHIP_ID_REG         0x9E00
#define TOUCH_DATA_REG            0x0000


// DATA
#define TOUCH_PACKET_SIZE 0x0FU
// index for touch data
typedef enum {
  TD_IDX_REV0,            /*  0: Reserved: default 0 */
  TD_IDX_REV1,            /*  1: Reserved: default 0 */
  TD_IDX_TD_STAT,         /*  2: The number of touch points */
  TD_IDX_P0_EVENT = 0x03, /*  3: Point 0 touch event, in high 4 bits [7:4],  */
  TD_IDX_P0_XH = 0x03,    /*  3: Point 0 X coordinate high bits, in low 4 bits[3:0] */
  TD_IDX_P0_XL,           /*  4: Point 0 X coordinate low bits */
  TD_IDX_P0_ID = 0x05,    /*  5: Point 0 touch id, in high 4 bits [7:4] */
  TD_IDX_P0_YH = 0x05,    /*  5: Point 0 Y coordinate high bits, in low bits[3:0]*/
  TD_IDX_P0_YL,           /*  6: Point 0 Y coordinate low bits */
  TD_IDX_P0_WEIGHT,       /*  7: Point 0 touch Weight(pressure) */
  TD_IDX_P0_AREA,         /*  8: Point 0 touch area */
  TD_IDX_P1_EVENT = 0x09, /*  9: Point 1 touch event, in high 4 bits [7:4],  */
  TD_IDX_P1_XH = 0x09,    /*  9: Point 1 X coordinate high bits, in low 4 bits[3:0] */
  TD_IDX_P1_XL,           /* 10: Point 1 X coordinate low bits */
  TD_IDX_P1_ID = 0x0B,    /* 11: Point 1 touch id, in high 4 bits [7:4] */
  TD_IDX_P1_YH = 0x0B,    /* 11: Point 1 Y coordinate high bits, in low bits[3:0]*/
  TD_IDX_P1_YL,           /* 12: Point 1 Y coordinate low bits */
  TD_IDX_P1_WEIGHT,       /* 13: Point 1 touch Weight(pressure) */
  TD_IDX_P1_AREA,         /* 14: Point 1 touch area */
} TOUCH_DATA_ITEM_INDEX;

typedef enum {
  TD_EVENT_PUTDOWN = 0x00,  /* touch down */
  TD_EVENT_PUTUP = 0x04,    /* touch up */
  TD_EVENT_CONTACT = 0x08,  /* touch contact */
}TOUCH_EVENT;

#define TD_STAT(DATA) DATA[TD_IDX_TD_STAT]

#define TD_POINT(DATA, P, C) (((uint32_t)DATA[TD_IDX_##P##_##C##H] & 0x0F) << 8) | ((uint32_t)DATA[TD_IDX_##P##_##C##L])
#define TD_POINT_EVENT(DATA, P) (DATA[TD_IDX_##P##_EVENT] & 0xF0) >> 4
#define TD_POINT_WEIGHT(DATA, P) DATA[TD_IDX_##P##_WEIGHT]
#define TD_POINT_AREA(DATA, P) DATA[TD_IDX_##P##_AREA]

#define TD_P0_X(DATA) TD_POINT(DATA, P0, X)
#define TD_P0_Y(DATA) TD_POINT(DATA, P0, Y)
#define TD_P0_EVENT(DATA) TD_POINT_EVENT(DATA, P0)
#define TD_P0_WEIGHT(DATA) TD_POINT_WEIGHT(DATA, P0)
#define TD_P0_AREA(DATA) TD_POINT_AREA(DATA, P0)

#define TD_P1_X(DATA) TD_POINT(DATA, P1, X)
#define TD_P1_Y(DATA) TD_POINT(DATA, P1, Y)
#define TD_P1_EVENT(DATA) TD_POINT_EVENT(DATA, P1)
#define TD_P1_WEIGHT(DATA) TD_POINT_WEIGHT(DATA, P1)
#define TD_P1_AREA(DATA) TD_POINT_AREA(DATA, P1)

void touch_init(void) {
  uint8_t id;
  i2c4_init();
  if (i2c4_read_reg16(TOUCH_ADDRESS, TOUCH_CHIP_ID_REG, &id, 1) != HAL_OK) {
    ensure(false, "touch init failed");
   }
}

void touch_power_on(void) { return; }

void touch_power_off(void) { return; }

void touch_sensitivity(uint8_t value) {
  // set panel threshold (TH_GROUP) - default value is 0x12
  // uint8_t touch_panel_threshold[] = {0x80, value};
  // ensure(sectrue *
  //            (HAL_OK == HAL_I2C_Master_Transmit(
  //                           &i2c_handle, TOUCH_ADDRESS, touch_panel_threshold,
  //                           sizeof(touch_panel_threshold), 10)),
  //        NULL);
}

uint32_t touch_is_detected(void) {
  return 1;
}

uint32_t touch_num_detected(void) {
  uint8_t data[TOUCH_PACKET_SIZE] = {0};
  if (i2c4_read_reg16(TOUCH_ADDRESS, TOUCH_DATA_REG, data, sizeof(data)) != HAL_OK) {
    return 0;
  }

  return data[TD_IDX_TD_STAT];
}

#define INVALID_TOUCH_POS 0xFFFFFFFF
#define ACCURACY 8
#define TOUCH_MAX_X 480
#define TOUCH_MAX_Y 800

// read touch data
//   the result is 0 or event, 0 means no event occurred and keep previous state
//   the state:
//         initial -> start -> [move | keep] | end -> ...
uint32_t touch_read(void) {
  static bool touching = false;
  static uint32_t prev_xy = INVALID_TOUCH_POS;

  uint8_t data[TOUCH_PACKET_SIZE];
  uint32_t xy;
  if (i2c4_try_lock() != 0) {
    return 0;
  }
  if (i2c4_read_reg16(TOUCH_ADDRESS, TOUCH_DATA_REG, data, sizeof(data)) != HAL_OK) {
    i2c4_unlock();
    return 0;
  }
  i2c4_unlock();

  int count = TD_STAT(data);

  // 1. count == 0
  //   1.1 touching == true, end
  //   1.1 touching == false, not have event
  // 2. count > 0
  //   2.1 touching == false, start
  //   2.2 touching == true, continue

  if (count == 0) {
    if (!touching) {
      // no event
      // keep previous state.
      return 0;
    }

    xy = prev_xy & 0xFFFFFF;
    touching = false;
    prev_xy = INVALID_TOUCH_POS;
    return TOUCH_END | xy;

  }

  uint16_t x = TD_P0_X(data);
  uint16_t y = TD_P0_Y(data);

  if (x > TOUCH_MAX_X || y > TOUCH_MAX_Y) {
    // ignore invalid touch data, keep previous state
    return 0;
  }
  xy = touch_pack_xy(x, y);
  uint16_t prev_x = touch_unpack_x(prev_xy);
  uint16_t prev_y = touch_unpack_y(prev_xy);

  if (!touching) {
    touching = true;
    prev_xy = xy;
    return TOUCH_START | xy;
  }

  if (abs(x - prev_x) > ACCURACY || abs(y - prev_y) > ACCURACY) {
    prev_xy = xy;
    return TOUCH_MOVE | xy;
  }

  return 0;
}

uint32_t touch_click(void) {
  uint32_t r = 0;
  r = touch_read();
  while (r) {
    r = touch_read();
    if ((r & TOUCH_END) == TOUCH_END) {
      break;
    }
  }

  return r;
}

uint32_t boot_touch_detect(uint32_t timeout) {
  uint32_t data, x_start, y_start, x_mov, y_mov;
  x_start = y_start = x_mov = y_mov = 0;

  for (int i = 0; i < timeout; i++) {
    data = touch_read();
    if (data != 0) {
      if (data & TOUCH_START) {
        x_start = x_mov = (data >> 12) & 0xFFF;
        y_start = y_mov = data & 0xFFF;
      }

      if (data & TOUCH_MOVE) {
        x_mov = (data >> 12) & 0xFFF;
        y_mov = data & 0xFFF;
      }

      if ((abs(x_start - x_mov) > 100) || (abs(y_start - y_mov) > 100)) {
        return 1;
      }
    }
    hal_delay(1);
  }

  return 0;
}

void touch_test(void) {
  int pos;
  int i = 0;
  while (1) {
    pos = touch_read();
    if (pos & TOUCH_START) {
      display_printf(" %d touch start x= %d,y=%d \n", i, (pos >> 12) & 0xfff,
                     pos & 0xfff);
    }
    if (pos & TOUCH_MOVE) {
      display_printf(" %d touch move x= %d,y=%d \n", i, (pos >> 12) & 0xfff,
                     pos & 0xfff);
    }
    if (pos & TOUCH_END) {
      display_printf(" %d touch end x= %d,y=%d \n", i, (pos >> 12) & 0xfff,
                     pos & 0xfff);
    }
    i++;
  }
}
