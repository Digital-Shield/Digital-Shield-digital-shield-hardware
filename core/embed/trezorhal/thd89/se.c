#include "thd89/se.h"

#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>

#include "stm32h7xx_hal.h"
#include "thd89.h"
#include "se_spi.h"
#include "alignment.h"

typedef enum {
  // 设备相关指令
  CMD_ID_GET_VERSION = 0x00,
  CMD_ID_GET_STATE = 0x01,
  CMD_ID_GET_LIFE_CYCLE = 0x02,
  CMD_ID_GET_SN = 0x03,
  CMD_ID_GET_DEV_PUBKEY = 0x04,
  CMD_ID_GET_DEV_CERT = 0x05,
  CMD_ID_DEV_SIGN = 0x06,
}command_id_t;

// struct for command and response
typedef struct {
  uint8_t cmd;
  uint8_t len[2];
  uint8_t payload[0];
} __attribute__((packed)) request_t;

typedef struct {
  uint8_t code;
  uint8_t len[2];
  uint8_t payload[0];
} __attribute__((packed)) response_t;

static inline size_t request_get_length(const request_t* req) {
  return GET_UINT16_BE(req->len, 0);
}
static inline void request_set_length(request_t* req, size_t len) {
  PUT_UINT16_BE(len, req->len, 0);
}

static inline size_t response_get_length(const response_t* resp) {
  return GET_UINT16_BE(resp->len, 0);
}
static inline void response_set_length(response_t* resp, size_t len) {
  PUT_UINT16_BE(len, resp->len, 0);
}

#define REQ_INIT_CMD(BUF, CMD) request_t *req = (void *)BUF; req->cmd = CMD
#define REQ_EMPTY_PAYLOAD(req) request_set_length(req, 0)
#define REQ_PAYLOAD(req, __payload__, __len__) \
  do {                                         \
    memcpy(req->payload, __payload__, __len__); \
    request_set_length(req, __len__);          \
  } while (0)

#define RESP_INIT(addr) response_t* resp = (void*)(addr)

typedef enum {
  RESP_CODE_SUCCESS = 0,
  RESP_CODE_INTERNAL_FAILED,
  RESP_CODE_INVALID_STATE,
  RESP_CODE_INVALID_PARAM_DATA,
  RESP_CODE_UNSUPPORTED_COMMAND,
  RESP_CODE_OBJECT_ALREADY_EXIST,
  RESP_CODE_OBJECT_NOT_EXIST,
} response_code_t;

char *se_get_version(void) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_VERSION);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return NULL;
    }
    RESP_INIT(response);
    // command result
    if (resp->code != RESP_CODE_SUCCESS) {
        return NULL;
    }
    if (response_get_length(resp) != 4) {
        return NULL;
    }
    struct {
        uint8_t major;
        uint8_t minor;
        uint8_t patch;
        uint8_t build;
    } *v = (void*)resp->payload;
    static char version[17] = {0};
    sprintf(version, "%d.%d.%d.%d", v->major, v->minor, v->patch, v->build);
    return version;
}

bool se_get_sn(char **serial) {
    *serial = NULL;
    return false;
}

bool se_setSeedStrength(uint32_t strength) {
    (void)strength; // Prevent unused parameter warning
    return false;
}

bool se_getSeedStrength(uint32_t *strength) {
    *strength = 0;
    return false;
}

bool se_importSeed(uint8_t *seed) {
    (void)seed; // Prevent unused parameter warning
    return false;
}

bool se_export_seed(uint8_t *seed) {
    (void)seed; // Prevent unused parameter warning
    return false;
}

void se_get_status(void) {
    // Empty implementation
}

bool se_hasPin(void) {
    return false;
}

bool se_verifyPin(const char *pin) {
    (void)pin; // Prevent unused parameter warning
    return false;
}

bool se_setPin(const char *pin) {
    (void)pin; // Prevent unused parameter warning
    return false;
}

bool se_changePin(const char *old_pin, const char *new_pin) {
    (void)old_pin; // Prevent unused parameter warning
    (void)new_pin; // Prevent unused parameter warning
    return false;
}

bool se_reset_pin(void) {
    return false;
}

bool se_isInitialized(void) {
    return false;
}

bool se_is_wiping(void) {
    return false;
}

void se_set_wiping(bool flag) {
    (void)flag; // Prevent unused parameter warning
}

void se_reset_state(void) {
    // Empty implementation
}

void se_reset_storage(void) {
    // Empty implementation
}

uint32_t se_pinFailedCounter(void) {
    return 0;
}

typedef struct
{
    uint8_t tag[4]; // SK PK or CERT
    uint32_t length; // length of item
    uint8_t data[0]; // item data
}se_obj_t;

typedef struct {
    uint8_t magic[16]; // 'SE-STORAGE'
    uint8_t sk[128]; // SK item
    uint8_t pk[256]; // PK item
    uint8_t cert[2048]; // cert item
} se_storage_t;

#define SE_STORAGE_FILED_SIZE(filed) sizeof(((se_storage_t *)0)->filed)

#define SE_STORAGE_MAGIC "SE-STORAGE"

#include "flash.h"
#include "stddef.h"
#include "rand.h"
#include "string.h"
#include "common.h"
#include "nist256p1.h"
#include "ecdsa.h"
#include "sha2.h"

static const void* se_storage_ptr(uint32_t offset, uint32_t size) {
    return flash_get_address(FLASH_SECTOR_SE_STORAGE, offset, size);
}
#define se_storage_magic_ptr() se_storage_ptr(offsetof(se_storage_t, magic), SE_STORAGE_FILED_SIZE(magic))
#define se_storage_sk_ptr() se_storage_ptr(offsetof(se_storage_t, sk), SE_STORAGE_FILED_SIZE(sk))
#define se_storage_pk_ptr() se_storage_ptr(offsetof(se_storage_t, pk), SE_STORAGE_FILED_SIZE(pk))
#define se_storage_cert_ptr() se_storage_ptr(offsetof(se_storage_t, cert), SE_STORAGE_FILED_SIZE(cert))

static void se_storage_write_bytes(uint32_t offset, const uint8_t *data, size_t len) {
    ensure(flash_unlock_write(), NULL);
    while (len--)
    {
        ensure(flash_write_byte(FLASH_SECTOR_SE_STORAGE, offset++, *data++), "se storage write failed");
    }
    ensure(flash_lock_write(), NULL);
}

#define se_storage_write_magic() se_storage_write_bytes(offsetof(se_storage_t, magic), (uint8_t*)SE_STORAGE_MAGIC, sizeof(SE_STORAGE_MAGIC))
#define se_storage_write_sk(buf, len) se_storage_write_bytes(offsetof(se_storage_t, sk), buf, len)
#define se_storage_write_pk(buf, len) se_storage_write_bytes(offsetof(se_storage_t, pk), buf, len)
#define se_storage_write_cert(buf, len) se_storage_write_bytes(offsetof(se_storage_t, cert), buf, len)

static void se_storage_init(void) {
    const se_storage_t *storage = flash_get_address(FLASH_SECTOR_SE_STORAGE, 0, sizeof(se_storage_t));
    // check magic
    if (memcmp(storage->magic, SE_STORAGE_MAGIC, sizeof(SE_STORAGE_MAGIC)) == 0) {
        return ;
    }
    se_storage_write_magic();

    // generate a new key pair
    uint8_t sk[32 + 4 + 4] = {0};
    se_obj_t *obj = (se_obj_t *)sk;
    obj->tag[0] = 'S';
    obj->tag[1] = 'K';
    obj->tag[2] = 0;
    obj->tag[3] = 0;
    obj->length = 32;
    do {
        random_buffer(obj->data, 32);
        // check
        if (0 == memcmp( obj->data, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 32))
            continue;
        if (0 <= memcmp( obj->data, "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE\xBA\xAE\xDC\xE6\xAF\x48\xA0\x3B\xBF\xD2\x5E\x8C\xD0\x36\x41\x41", 32))
            continue;
        break;
    }while (1);
    se_storage_write_sk(sk, sizeof(sk));

    uint8_t pk[65 + 4 + 4] = {0};
    obj = (se_obj_t *)pk;
    obj->tag[0] = 'P';
    obj->tag[1] = 'K';
    obj->tag[2] = 0;
    obj->tag[3] = 0;
    obj->length = 65;
    ecdsa_get_public_key65(&nist256p1, sk+8, obj->data);
    se_storage_write_pk(pk, sizeof(pk));
}

bool se_device_init(uint8_t mode, const char *passphrase) {
    (void)mode; // Prevent unused parameter warning
    (void)passphrase; // Prevent unused parameter warning
    return false;
}

bool se_get_pubkey(uint8_t pubkey[65]) {
    se_obj_t *obj = (se_obj_t *)se_storage_pk_ptr();
    if (memcmp(obj->tag, "PK", 2) != 0) {
        return false;
    }
    memcpy(pubkey, obj->data, 65);
    return true;
}

bool se_write_certificate(const uint8_t *cert, uint32_t cert_len) {
    if(cert_len > SE_STORAGE_FILED_SIZE(cert) - 8) {
        return false;
    }
    se_obj_t *obj = (se_obj_t *)se_storage_cert_ptr();
    if (memcmp(obj->tag, "CERT", 4) == 0) {
        return false;
    }

    uint8_t _cert[SE_STORAGE_FILED_SIZE(cert)] = {0};
    obj = (se_obj_t *)_cert;
    obj->tag[0] = 'C';
    obj->tag[1] = 'E';
    obj->tag[2] = 'R';
    obj->tag[3] = 'T';
    obj->length = cert_len;
    memcpy(obj->data, cert, cert_len);
    se_storage_write_cert(_cert, sizeof(_cert));
    return true;
}

bool se_get_certificate_len(uint32_t *cert_len) {
    *cert_len = 0;
    se_obj_t *obj = (se_obj_t *)se_storage_cert_ptr();
    if (memcmp(obj->tag, "CERT", 4) != 0) {
        return false;
    }
    *cert_len = obj->length;
    return true;
}

bool se_read_certificate(uint8_t *cert, uint32_t *cert_len) {
    se_obj_t *obj = (se_obj_t *)se_storage_cert_ptr();
    if (memcmp(obj->tag, "CERT", 4) != 0) {
        *cert_len = 0;
        return false;
    }
    if (*cert_len < obj->length) {
        *cert_len = obj->length;
        return false;
    }
    memcpy(cert, obj->data, obj->length);
    *cert_len = obj->length;
    return true;
}

bool se_sign_message(uint8_t *msg, uint32_t msg_len, uint8_t *signature) {
    // 1. digest(msg)
    uint8_t digest[32] = {0};
    sha256_Raw(msg, msg_len, digest);

    // 2. get sk
    se_obj_t *obj = (se_obj_t *)se_storage_sk_ptr();
    if (memcmp(obj->tag, "SK", 2) != 0) {
        return false;
    }

    // 2. sign
    ecdsa_sign_digest(&nist256p1, obj->data, digest, signature, NULL, NULL);
    return true;
}

void se_init(void) {
    // Empty implementation
    (void) se_storage_init;
    se_spi_init();
    thd89_init();
    // reset thd89 connection
    thd89_reset();
}

void se_test(void) {
    se_init();
    while (1) {
        HAL_Delay(1000);
        char* version = se_get_version();
        printf("version: %s\n", version);
    }

}
