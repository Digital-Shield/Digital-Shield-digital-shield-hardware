#include "lv_font_ex.h"

// Source Han Sans,Bold, 26
static binary_font_t binary_26 = {
    .path = "/res/lv_font_source_han_bold_26.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_bold_26 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 26,
    .base_line = 3,
    .user_data = &binary_26,
};

// Source Han Sans,Bold, 30
static binary_font_t binary_30 = {
    .path = "/res/lv_font_source_han_bold_30.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_bold_30 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 30,
    .base_line = 3,
    .user_data = &binary_30,
};

// Source Han Sans,Bold, 38
static binary_font_t binary_38 = {
    .path = "/res/lv_font_source_han_bold_38.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_bold_38 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 30,
    .base_line = 3,
    .user_data = &binary_38,
};

// Source Han Sans,Med, 28
static binary_font_t binary_med_28 = {
    .path = "/res/lv_font_source_han_med_28.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_med_28 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 28,
    .base_line = 3,
    .user_data = &binary_med_28,
};

// Source Han Sans,Med, 32
static binary_font_t binary_med_32 = {
    .path = "/res/lv_font_source_han_med_32.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_med_32 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 32,
    .base_line = 3,
    .user_data = &binary_med_32,
};

// Source Han Sans,Med, 40
static binary_font_t binary_med_40 = {
    .path = "/res/lv_font_source_han_med_40.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_med_40 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 40,
    .base_line = 3,
    .user_data = &binary_med_40,
};

// Source Han Sans,Reg, 24
static binary_font_t binary_reg_24 = {
    .path = "/res/lv_font_source_han_reg_24.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_reg_24 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 24,
    .base_line = 3,
    .user_data = &binary_reg_24,
};

// Source Han Sans,Reg, 26
static binary_font_t binary_reg_26 = {
    .path = "/res/lv_font_source_han_reg_26.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_reg_26 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 26,
    .base_line = 3,
    .user_data = &binary_reg_26,
};

// Source Han Sans,Reg, 28
static binary_font_t binary_reg_28 = {
    .path = "/res/lv_font_source_han_reg_28.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_reg_28 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 28,
    .base_line = 3,
    .user_data = &binary_reg_28,
};

// Source Han Sans,Reg, 30
static binary_font_t binary_reg_30 = {
    .path = "/res/lv_font_source_han_reg_30.bin",
    .f = NULL,
    .glyph_location = 0,
    .xbf = {
        .min = 0x20,
        .max = 0xFFFF,
        .bpp = 4,
    },
};

const lv_font_t lv_font_scs_reg_30 = {
    .get_glyph_bitmap = user_font_get_bitmap,
    .get_glyph_dsc = user_font_get_glyph_dsc,
    .line_height = 30,
    .base_line = 3,
    .user_data = &binary_reg_30,
};