#include "lv_font_ex.h"

#include <stdio.h>
#include <stdint.h>

#include "lvgl.h"

#define FONT_BIN_FILE FONT_DIR"/res/lv_font_source_han_bold_30.bin"

static x_header_t __g_xbf_hd = {
    .min = 0x0020,
    .max = 0xffff,
    .bpp = 4,
};

static FILE* f = NULL;
static uint32_t glyph_location = 0;

static font_data_cache font_cache = {0};

static void __exit(void) {
  fclose(f);
}
static int __user_font_getdata(uint8_t *data_buf, int offset, int size) {
  int ret;
  if (!f) {
    uint8_t buf[4] = {0};
    uint32_t len = 0;
    f = fopen(FONT_BIN_FILE, "r");
    if (!f) {
      return -1;
    }
    ret  = fseek(f, LOCA_OFFSET, SEEK_SET);
    if (ret) {
      return -1;
    }
    atexit(__exit);
    ret = fread(&len, 1, 4, f);
    if (ret != 4) {
      return -1;
    }
    ret = fread(buf, 1, 4, f);
    if (ret != 4) {
      return -1;
    }
    if (memcmp("loca", buf, 4) != 0) {
      return -1;
    }
    glyph_location = len + LOCA_OFFSET;
  }
  ret = fseek(f, offset, SEEK_SET);
  if (ret) {
    return -1;
  }
  ret = fread(data_buf, 1, size, f);
  if (ret != size) {
    return -1;
  }
  return 0;
}

static const uint8_t *__user_font_get_bitmap(const lv_font_t *font,
                                             uint32_t unicode_letter) {
  if (unicode_letter > __g_xbf_hd.max || unicode_letter < __g_xbf_hd.min) {
    return NULL;
  }
  uint8_t *font_data = NULL;
  uint32_t data_len = 0;
  font_data = font_cache_get_letter(&font_cache, unicode_letter, &data_len);
  if (font_data) {
    return font_data + sizeof(glyph_dsc_t);
  } else {
    uint32_t unicode_offset = (unicode_letter - __g_xbf_hd.min + 1) * 4;
    uint32_t len = 0;
    uint8_t buf[8] = {0};
    __user_font_getdata(buf, unicode_offset + LOCA_OFFSET + LOCA_VALUE_OFFSET,
                        8);
    uint32_t *p_pos = (uint32_t *)buf;
    if (p_pos[0] != 0) {
      len = p_pos[1] - p_pos[0];
      font_data = font_malloc(len);
      if (__user_font_getdata(font_data, glyph_location + p_pos[0], len) != 0) {
        return NULL;
      }
      font_cache_add_letter(&font_cache, unicode_letter, font_data, len);
      return font_data + sizeof(glyph_dsc_t);
    } else {
      return NULL;
    }
  }

  return NULL;
}

static bool __user_font_get_glyph_dsc(const lv_font_t *font,
                                      lv_font_glyph_dsc_t *dsc_out,
                                      uint32_t unicode_letter,
                                      uint32_t unicode_letter_next) {
  if (unicode_letter > __g_xbf_hd.max || unicode_letter < __g_xbf_hd.min) {
    return NULL;
  }

  uint8_t *font_data = NULL;
  uint32_t data_len = 0;
  font_data = font_cache_get_letter(&font_cache, unicode_letter, &data_len);
  if (font_data) {
  } else {
    uint32_t unicode_offset = (unicode_letter - __g_xbf_hd.min + 1) * 4;
    uint32_t len = 0;
    uint8_t buf[8] = {0};
    __user_font_getdata(buf, unicode_offset + LOCA_OFFSET + LOCA_VALUE_OFFSET,
                        8);
    uint32_t *p_pos = (uint32_t *)buf;
    if (p_pos[0] != 0) {
      len = p_pos[1] - p_pos[0];
      font_data = font_malloc(len);
      if (__user_font_getdata(font_data, glyph_location + p_pos[0], len) != 0) {
        return false;
      }
      font_cache_add_letter(&font_cache, unicode_letter, font_data, len);
    } else {
      return false;
    }
  }
  glyph_dsc_t *gdsc = (glyph_dsc_t *)font_data;
  dsc_out->adv_w = (gdsc->adv_w + (1 << 3)) >> 4;
  dsc_out->box_h = gdsc->box_h;
  dsc_out->box_w = gdsc->box_w;
  dsc_out->ofs_x = gdsc->ofs_x;
  dsc_out->ofs_y = gdsc->ofs_y;
  dsc_out->bpp = __g_xbf_hd.bpp;
  return true;
}

// Source Han Sans,Bold,30
const lv_font_t lv_font_scs_bold_30 = {
    .get_glyph_bitmap = __user_font_get_bitmap,
    .get_glyph_dsc = __user_font_get_glyph_dsc,
    .line_height = 30,
    .base_line = 3,
};
