#ifndef TREZORHAL_CAMERA_H
#define TREZORHAL_CAMERA_H
#include <stdint.h>
#include "secbool.h"
enum {
  CAMERA_POWER_OFF,
  CMAERA_POWER_ON,
};

enum {
  CAMERA_QR_TYPE_NUMBER = 1,
  CAMERA_QR_TYPE_STRING = 2,
  CAMERA_QR_TYPE_BYTES  = 4,
};

secbool camera_init(int width, int height);
void camera_start(void);
// only suspend camera capturing
void camera_suspend(void);
// resume camera capturing
void camera_resume(void);
void camera_stop(void);
// suspend camera capturing and not show preview
void camera_hide(void);
// resume camera capturing and show preview
void camera_show(void);
void camera_deinit(void);
void camera_led_on(void);
void camera_led_off(void);

secbool camera_is_power_on(void);

secbool camera_is_captured(void);

int camera_scan_qrcode(uint8_t qrcode[1024 + 1], int* type);
#endif
