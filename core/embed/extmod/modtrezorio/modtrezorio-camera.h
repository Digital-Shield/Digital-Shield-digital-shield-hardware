#include <stdio.h>
#include "camera.h"
#include "embed/extmod/trezorobj.h"
#include "mpconfigport.h"
#include "sdram.h"
#include "secbool.h"

/// package: trezorio.__init__

/// class Camera:
///     """
///     Camera configuration.
///     """
///     NONE: int = 0
///     INIT: int = 1
///     STOPPED: int = 2
///     SUSPENDED: int = 3
///     CAPTURING: int = 4
///     def __init__(self, iface_num: int, width: int, height: int) -> None:
///         ...
///     def iface_num(self) -> int:
///         ...
///     def init(self) -> None:
///         ...
///     def deinit(self) -> None:
///         ...
///     def start(self) -> None:
///         ...
///     def stop(self) -> None:
///         ...
///     def suspend(self) -> None:
///         ...
///     def resume(self) -> None:
///         ...
///     def hide(self) -> None:
///         ...
///     def show(self) -> None:
///         ...
///     def led_on(self) -> None:
///         ...
///     def led_off(self) -> None:
///         ...
///     def led_toggle(self) -> None:
///         ...
///     def led_state(self) -> int:
///         ...
///     def buffer(self) -> bytes:
///         ...
///     def state(self) -> int:
///         ...
///     def width(self) -> int:
///         ...
///     def height(self) -> int:
///         ...

enum {
  CAMERA_STATE_NONE,
  CAMERA_STATE_INIT,
  CAMERA_STATE_STOPPED,
  CAMERA_STATE_SUSPENDED,
  CAMERA_STATE_CAPTURING,
};

enum {
  CAMERA_LED_OFF,
  CAMERA_LED_ON,
};

typedef struct _mp_obj_Camera_t {
  mp_obj_base_t base;
  mp_int_t iface_num;
  mp_int_t width;
  mp_int_t height;

  mp_int_t state;
  mp_int_t led_state;
  mp_obj_t buffer;
} mp_obj_Camera_t;

static mp_obj_t mod_trezorio_Camera_make_new(const mp_obj_type_t *type,
                                             size_t n_args, size_t n_kw,
                                             const mp_obj_t *args) {
  mp_arg_check_num(n_args, n_kw, 3, 3, false);

  const mp_int_t iface_num = mp_obj_get_int(args[0]);
  const mp_int_t width = mp_obj_get_int(args[1]);
  const mp_int_t height = mp_obj_get_int(args[2]);

  mp_obj_Camera_t *o = m_new_obj(mp_obj_Camera_t);
  o->base.type = type;

  o->iface_num = iface_num;
  o->width = width;
  o->height = height;

  o->state = CAMERA_STATE_NONE;
  o->led_state = CAMERA_LED_OFF;

  // create buffer object from camera captured buffer, bytearray type
  // buffer is 16bit RGB565 format
  o->buffer = mp_obj_new_bytearray_by_ref(
      width * height * 2, (uint8_t *)FMC_SDRAM_IMAGE_BUFFER_ADDRESS);

  return MP_OBJ_FROM_PTR(o);
}

// iface_num
static mp_obj_t mod_trezorio_Camera_iface_num(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return MP_OBJ_NEW_SMALL_INT(o->iface_num);
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_iface_num_obj,
                                 mod_trezorio_Camera_iface_num);

// width
static mp_obj_t mod_trezorio_Camera_width(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return MP_OBJ_NEW_SMALL_INT(o->width);
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_width_obj,
                                 mod_trezorio_Camera_width);

// height
static mp_obj_t mod_trezorio_Camera_height(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return MP_OBJ_NEW_SMALL_INT(o->height);
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_height_obj,
                                 mod_trezorio_Camera_height);

// buffer
static mp_obj_t mod_trezorio_Camera_buffer(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return o->buffer;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_buffer_obj,
                                 mod_trezorio_Camera_buffer);

// state
static mp_obj_t mod_trezorio_Camera_state(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return MP_OBJ_NEW_SMALL_INT(o->state);
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_state_obj,
                                 mod_trezorio_Camera_state);

// init
static mp_obj_t mod_trezorio_Camera_init(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);

  // init camera
  if (camera_init(o->width, o->height) != sectrue) {
    printf("can't power on camera\n");
  }

  o->state = CAMERA_STATE_INIT;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_init_obj,
                                 mod_trezorio_Camera_init);

// deinit
static mp_obj_t mod_trezorio_Camera_deinit(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);

  // deinit camera
  camera_deinit();

  o->state = CAMERA_STATE_NONE;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_deinit_obj,
                                 mod_trezorio_Camera_deinit);

// start
static mp_obj_t mod_trezorio_Camera_start(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);

  // start camera
  camera_start();

  o->state = CAMERA_STATE_CAPTURING;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_start_obj,
                                 mod_trezorio_Camera_start);

// stop
static mp_obj_t mod_trezorio_Camera_stop(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);

  // stop camera
  camera_stop();

  o->state = CAMERA_STATE_STOPPED;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_stop_obj,
                                 mod_trezorio_Camera_stop);

// suspend
static mp_obj_t mod_trezorio_Camera_suspend(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  // suspend camera
  camera_suspend();

  o->state = CAMERA_STATE_SUSPENDED;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_suspend_obj,
                                 mod_trezorio_Camera_suspend);

// resume
static mp_obj_t mod_trezorio_Camera_resume(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  // resume camera
  camera_resume();

  o->state = CAMERA_STATE_CAPTURING;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_resume_obj,
                                 mod_trezorio_Camera_resume);

// hide
static mp_obj_t mod_trezorio_Camera_hide(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  // hide camera
  camera_hide();

  o->state = CAMERA_STATE_SUSPENDED;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_hide_obj,
                                 mod_trezorio_Camera_hide);

// show
static mp_obj_t mod_trezorio_Camera_show(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  // show camera
  camera_show();
  o->state = CAMERA_STATE_CAPTURING;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_show_obj,
                                 mod_trezorio_Camera_show);

// led_on
static mp_obj_t mod_trezorio_Camera_led_on(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  camera_led_on();
  o->led_state = CAMERA_LED_ON;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_led_on_obj,
                                 mod_trezorio_Camera_led_on);

// led_off
static mp_obj_t mod_trezorio_Camera_led_off(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  camera_led_off();
  o->led_state = CAMERA_LED_OFF;
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_led_off_obj,
                                 mod_trezorio_Camera_led_off);

// led_toggle
static mp_obj_t mod_trezorio_Camera_led_toggle(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  if (o->led_state == CAMERA_LED_ON) {
    camera_led_off();
    o->led_state = CAMERA_LED_OFF;
  } else if (o->led_state == CAMERA_LED_OFF) {
    camera_led_on();
    o->led_state = CAMERA_LED_ON;
  }
  return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_led_toggle_obj,
                                 mod_trezorio_Camera_led_toggle);
// led_state
static mp_obj_t mod_trezorio_Camera_led_state(mp_obj_t self) {
  mp_obj_Camera_t *o = MP_OBJ_TO_PTR(self);
  return MP_OBJ_NEW_SMALL_INT(o->led_state);
}
static MP_DEFINE_CONST_FUN_OBJ_1(mod_trezorio_Camera_led_state_obj,
                                 mod_trezorio_Camera_led_state);

static const mp_rom_map_elem_t mod_trezorio_Camera_locals_dict_table[] = {
    // iface_num
    {MP_ROM_QSTR(MP_QSTR_iface_num), MP_ROM_PTR(&mod_trezorio_Camera_iface_num_obj)},
    // init
    {MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&mod_trezorio_Camera_init_obj)},
    // deinit
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&mod_trezorio_Camera_deinit_obj)},
    // start
    {MP_ROM_QSTR(MP_QSTR_start), MP_ROM_PTR(&mod_trezorio_Camera_start_obj)},
    // stop
    {MP_ROM_QSTR(MP_QSTR_stop), MP_ROM_PTR(&mod_trezorio_Camera_stop_obj)},
    // suspend
    {MP_ROM_QSTR(MP_QSTR_suspend), MP_ROM_PTR(&mod_trezorio_Camera_suspend_obj)},
    // resume
    {MP_ROM_QSTR(MP_QSTR_resume), MP_ROM_PTR(&mod_trezorio_Camera_resume_obj)},
    // hide
    {MP_ROM_QSTR(MP_QSTR_hide), MP_ROM_PTR(&mod_trezorio_Camera_hide_obj)},
    // show
    {MP_ROM_QSTR(MP_QSTR_show), MP_ROM_PTR(&mod_trezorio_Camera_show_obj)},
    // led_on
    {MP_ROM_QSTR(MP_QSTR_led_on), MP_ROM_PTR(&mod_trezorio_Camera_led_on_obj)},
    // led_off
    {MP_ROM_QSTR(MP_QSTR_led_off), MP_ROM_PTR(&mod_trezorio_Camera_led_off_obj)},
    // led_toggle
    {MP_ROM_QSTR(MP_QSTR_led_toggle), MP_ROM_PTR(&mod_trezorio_Camera_led_toggle_obj)},
    // led_state

    // width
    {MP_ROM_QSTR(MP_QSTR_width), MP_ROM_PTR(&mod_trezorio_Camera_width_obj)},
    // height
    {MP_ROM_QSTR(MP_QSTR_height), MP_ROM_PTR(&mod_trezorio_Camera_height_obj)},
    // buffer
    {MP_ROM_QSTR(MP_QSTR_buffer), MP_ROM_PTR(&mod_trezorio_Camera_buffer_obj)},
    // state
    {MP_ROM_QSTR(MP_QSTR_state), MP_ROM_PTR(&mod_trezorio_Camera_state_obj)},
    // led_state
    {MP_ROM_QSTR(MP_QSTR_led_state), MP_ROM_PTR(&mod_trezorio_Camera_led_state_obj)},

    // states
    {MP_ROM_QSTR(MP_QSTR_NONE), MP_ROM_INT(CAMERA_STATE_NONE)},
    {MP_ROM_QSTR(MP_QSTR_INIT), MP_ROM_INT(CAMERA_STATE_INIT)},
    {MP_ROM_QSTR(MP_QSTR_STOPPED), MP_ROM_INT(CAMERA_STATE_STOPPED)},
    {MP_ROM_QSTR(MP_QSTR_SUSPENDED), MP_ROM_INT(CAMERA_STATE_SUSPENDED)},
    {MP_ROM_QSTR(MP_QSTR_CAPTURING), MP_ROM_INT(CAMERA_STATE_CAPTURING)},
    {MP_ROM_QSTR(MP_QSTR_LED_ON), MP_ROM_INT(CAMERA_LED_ON)},
    {MP_ROM_QSTR(MP_QSTR_LED_OFF), MP_ROM_INT(CAMERA_LED_OFF)},
};

static MP_DEFINE_CONST_DICT(mod_trezorio_Camera_locals_dict,
                            mod_trezorio_Camera_locals_dict_table);

static const mp_obj_type_t mod_trezorio_Camera_type = {
    {&mp_type_type},
    .name = MP_QSTR_Camera,
    .make_new = mod_trezorio_Camera_make_new,
    .locals_dict = (void *)&mod_trezorio_Camera_locals_dict,
};
