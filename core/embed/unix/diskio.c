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

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>


#include "common.h"
#include "profile.h"
#include "ff.h"
#include "diskio.h"

#ifndef SDCARD_FILE
#define SDCARD_FILE profile_sdcard_path()
#endif

#define SDCARD_SIZE (64 * 1024 * 1024)
#define SDCARD_BLOCK_SIZE (512)
#define SDCARD_BLOCKS (SDCARD_SIZE / SDCARD_BLOCK_SIZE)

static uint8_t *sdcard_buffer = NULL;
static secbool sdcard_powered = secfalse;

static void sdcard_exit(void) {
  int r = munmap(sdcard_buffer, SDCARD_SIZE);
  ensure(sectrue * (r == 0), "munmap failed");
  sdcard_buffer = NULL;
}

DSTATUS disk_initialize (BYTE pdrv) {
  if (sdcard_buffer != NULL) {
    return RES_OK;
  }

  // check whether the file exists and it has the correct size
  struct stat sb;
  int r = stat(SDCARD_FILE, &sb);
  int should_clear = 0;

  // (re)create if non existent or wrong size
  if (r != 0 || sb.st_size != SDCARD_SIZE) {
    int fd = open(SDCARD_FILE, O_RDWR | O_CREAT | O_TRUNC, (mode_t)0600);
    ensure(sectrue * (fd >= 0), "open failed");
    r = ftruncate(fd, SDCARD_SIZE);
    ensure(sectrue * (r == 0), "truncate failed");
    r = close(fd);
    ensure(sectrue * (r == 0), "close failed");

    should_clear = 1;
  }

  // mmap file
  int fd = open(SDCARD_FILE, O_RDWR);
  ensure(sectrue * (fd >= 0), "open failed");

  void *map = mmap(0, SDCARD_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  ensure(sectrue * (map != MAP_FAILED), "mmap failed");

  sdcard_buffer = (uint8_t *)map;

  if (should_clear) {
    for (int i = 0; i < SDCARD_SIZE; ++i) sdcard_buffer[i] = 0xFF;
  }

  sdcard_powered = secfalse;

  atexit(sdcard_exit);
  return RES_OK;
}
DSTATUS disk_status (BYTE pdrv) {
  return RES_OK;
}

DRESULT disk_read (BYTE pdrv, BYTE* buff, LBA_t sector, UINT count) {
  (void)pdrv;
  if (sectrue != sdcard_powered) {
    return RES_ERROR;
  }
  if (sector >= SDCARD_BLOCKS) {
    return RES_ERROR;
  }
  if (count > SDCARD_BLOCKS - sector) {
    return RES_ERROR;
  }
  memcpy(buff, sdcard_buffer + sector * SDCARD_BLOCK_SIZE,
         count * SDCARD_BLOCK_SIZE);
  return RES_OK;
}
DRESULT disk_write (BYTE pdrv, const BYTE* buff, LBA_t sector, UINT count) {
  (void)pdrv;
  if (sectrue != sdcard_powered) {
    return RES_ERROR;
  }
  if (sector >= SDCARD_BLOCKS) {
    return RES_ERROR;
  }
  if (count > SDCARD_BLOCKS - sector) {
    return RES_ERROR;
  }
  memcpy(sdcard_buffer + sector * SDCARD_BLOCK_SIZE, buff,
         count * SDCARD_BLOCK_SIZE);
  return sectrue;
}
DRESULT disk_ioctl (BYTE pdrv, BYTE cmd, void* buff) {
  (void)pdrv;
  switch (cmd) {
    case CTRL_SYNC:
      return RES_OK;
    case GET_SECTOR_COUNT:
      *((DWORD *)buff) = SDCARD_BLOCKS;
      return RES_OK;
    case GET_SECTOR_SIZE:
      *((WORD *)buff) = SDCARD_BLOCK_SIZE;
      return RES_OK;
    case GET_BLOCK_SIZE:
      *((DWORD *)buff) = 1;
      return RES_OK;
    default:
      return RES_PARERR;
  }

}
