#ifndef LV_FONT_EX_H
#define LV_FONT_EX_H

#include "secure_heap.h"

#define font_malloc pvPortMalloc
#define font_free vPortFree

#define FONT_CACHE __attribute__((section("sram1")))

// 缓存的fat文件不连续的簇数量，用于提高 f_seek 的速度
// 这个值和文件碎片化有关，文件碎片化越严重，需要缓存的数量越多
// SZ_TBL = 2 * N + 2 这里的 N是碎片数量，即不连续的簇的数量
// 经常反复写的文件一般碎片化比较严重，但对于字体文件，我们不会经常写，或者几乎写进去就不会再修改了
// 所以字体文件基本上都是连续存储的，也就是只有一个簇
// 假设不连续的簇为128（文件碎片化已经非常严重），这里只需要设置为 258
// 即使没有命中缓存，fat文件系统也是可以遍历文件查找到对应的数据，只是少慢一点
#define SZ_TBL 258

#define LOCA_OFFSET 0x4C
#define LOCA_VALUE_OFFSET 0x0C
#define GLYPH_OFFSET 0x08

typedef struct {
  uint16_t min;
  uint16_t max;
  uint8_t bpp;
  uint8_t reserved[3];
} x_header_t;

typedef struct __attribute__((packed)) {
  uint16_t adv_w;
  uint8_t box_w;
  uint8_t box_h;
  int8_t ofs_x;
  int8_t ofs_y;
} glyph_dsc_t;

#define FONT_CACHE_NUM 256

typedef struct {
  uint32_t unicode_letter;
  uint32_t data_size;
  uint8_t *data;
} font_info;

typedef struct {
  uint32_t cache_num;
  uint32_t cache_index;
  uint32_t cache_tail;
  font_info font_infos[FONT_CACHE_NUM];
} font_data_cache;

int font_cache_add_letter(font_data_cache *font_cache, uint32_t letter,
                          uint8_t *font_data, uint32_t data_len);
uint8_t *font_cache_get_letter(font_data_cache *font_cache, uint32_t letter,
                               uint32_t *buff_size);

#endif
