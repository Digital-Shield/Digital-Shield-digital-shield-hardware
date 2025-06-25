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
#include "sha2.h"
#include "device.h"

bool pcbv10_se_get_pubkey(uint8_t pubkey[65]);
bool pcbv10_se_get_certificate_len(size_t *cert_len);
bool pcbv10_se_read_certificate(uint8_t *cert, size_t *cert_len);
bool pcbv10_se_sign_message(uint8_t *msg, size_t msg_len, uint8_t *signature);

enum {
  // 设备相关指令
  CMD_ID_GET_VERSION = 0x00,
  CMD_ID_GET_STATE = 0x01,
  CMD_ID_GET_LIFE_CYCLE = 0x02,
  CMD_ID_GET_SN = 0x03,
  CMD_ID_GET_DEV_PUBKEY = 0x04,
  CMD_ID_GET_DEV_CERT_LENGTH = 0x05,
  CMD_ID_GET_DEV_CERT = 0x06,
  CMD_ID_DEV_SIGN = 0x07,

  // PIN 相关指令
  CMD_ID_HAS_PIN = 0x08,
  CMD_ID_SET_PIN = 0x09,
  CMD_ID_VERIFY_PIN = 0x0A,
  CMD_ID_CHANGE_PIN = 0x0B,
  CMD_ID_RESET_PIN = 0x0C,
  CMD_ID_GET_PIN_MAX_RETRY = 0x0D,
  CMD_ID_GET_PIN_RETRY = 0x0E,
  CMD_ID_FORGET_PIN = 0x0F,

  // 管理指令
  CMD_ID_REBOOT = 0x10,
  CMD_ID_LAUNCH = 0x11,
  CMD_ID_WIPE_USER_STORAGE = 0x12,

  // 文件指令
  CMD_ID_WRITE_FILE = 0x20,
  CMD_ID_READ_FILE = 0x21,
  CMD_ID_DELETE_FILE = 0x22,
  CMD_ID_GET_FILE_SIZE = 0x23,
  CMD_ID_SET_FILE_ACCESS = 0x24,

  // 密码算法指令
  CMD_ID_RANDOM = 0x30,
  CMD_ID_GEN_SECRET = 0x31,
  CMD_ID_GEN_KEY = 0x32,
  CMD_ID_SET_KEY = 0x33,
  CMD_ID_GEN_KEY_PAIR = 0x34,
  CMD_ID_GET_PUB_KEY = 0x35,
  CMD_ID_DERIVE_KEY = 0x36,

  CMD_ID_ENCRYPT_SYM = 0x40,
  CMD_ID_DECRYPT_SYM = 0x41,
  CMD_ID_ENCRYPT_ASYM = 0x42,
  CMD_ID_DECRYPT_ASYM = 0x43,
  CMD_ID_CMAC = 0x44,
  CMD_ID_HASH = 0x45,
  CMD_ID_HMAC = 0x46,
  CMD_ID_SIGN = 0x47,
  CMD_ID_VERIFY = 0x48,
  CMD_ID_ECDH = 0x49,

  // boot 指令
  CMD_ID_VERIFY_APP = 0x90,
  CMD_ID_INSTALL_APP = 0x91,

  CMD_ID_ROM_BL = 0xEF,
};
enum {
  CMD_PARAM_OLD_PIN = 0x00,
  CMD_PARAM_NEW_PIN = 0x01,
};

typedef enum {
  RESP_CODE_SUCCESS = 0,
  RESP_CODE_INTERNAL_FAILED,
  RESP_CODE_INVALID_STATE,
  RESP_CODE_INVALID_PARAM_DATA,
  RESP_CODE_UNSUPPORTED_COMMAND,
  RESP_CODE_OBJECT_ALREADY_EXIST,
  RESP_CODE_OBJECT_NOT_EXIST,
  RESP_CODE_PIN_LOCKED,
  RESP_CODE_ACCESS_DENIED,

  RESP_CODE_VERIFY_PIN_FAIL_X = 0x80,
} response_code_t;

#define CHECK_FID(id) do {          \
    if (id < OID_USER_OBJ_BASE) {   \
        return 1;                   \
    }                               \
} while (0)

#define CHECK_CMD_RESULT(ret) do {  \
    if (ret != 0) {     \
        return ret;                 \
    }                               \
} while (0)

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

typedef struct {
  uint8_t tag;
  uint8_t len[2];
  uint8_t data[0];
}__attribute__((packed))cmd_param_t;

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

static inline size_t command_size(const request_t* req) {
  return 3 + request_get_length(req);
}
static int se_execute_command(const uint8_t* command, uint8_t* response, size_t* response_size) {
    const request_t *req = (void*)command;
    size_t req_size = command_size(req);
    thd89_result_t ret = thd89_execute_command(command, req_size, response, *response_size, response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }

    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return resp->code;
    }
    return 0;
}

static int se_sample_command(uint8_t cmd_id) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, cmd_id);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_get_version(char version[17]) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_VERSION);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 4) {
        return 1;
    }
    struct {
        uint8_t major;
        uint8_t minor;
        uint8_t patch;
        uint8_t build;
    } *v = (void*)resp->payload;
    sprintf(version, "%d.%d.%d", v->major, v->minor, v->patch);
    return 0;
}

int se_get_sn(char serial[33]) {
    uint8_t command[3] = {0};
    uint8_t response[64] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_SN);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    memcpy(serial, resp->payload, response_get_length(resp));
    return 0;
}

int se_get_running_state(se_state_t *state) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_STATE);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    *state = (se_state_t)resp->payload[0];
    return 0;
}

int se_get_life_cycle(life_cycle_t *life_cycle) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_LIFE_CYCLE);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    *life_cycle = (life_cycle_t)resp->payload[0];
    return 0;
}

int se_reboot(void) {
    return se_sample_command(CMD_ID_REBOOT);
}

int se_launch(se_state_t state) {
    uint8_t command[4] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    // 注意 boot状态下只能启动 app, app状态下只能启动到boot
    // boot -> app, app -> boot
    // 其他状态下会失败
    REQ_INIT_CMD(command, CMD_ID_LAUNCH);
    REQ_PAYLOAD(req, &state, 1);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}
int se_back_to_rom_bl(void) {
    return se_sample_command(CMD_ID_ROM_BL);
}

int se_wipe_user_storage(void) {
    return se_sample_command(CMD_ID_WIPE_USER_STORAGE);
}

int se_write_file(uint16_t id, const uint8_t *data, size_t data_len) {
    uint8_t command[1024] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_WRITE_FILE);
    uint8_t *p = req->payload;
    // id
    PUT_UINT16_BE(id, p, 0);
    // move over `id`
    p += 2;

    // len
    PUT_UINT16_BE(data_len, p, 0);
    // move over `len`
    p += 2;

    memcpy(p, data, data_len);
    request_set_length(req, 4 + data_len);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}


int se_read_file(uint16_t id, uint8_t *data, size_t *data_len) {
    uint8_t command[16] = {0};
    uint8_t response[1024] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_READ_FILE);
    uint8_t *p = req->payload;
    // id
    PUT_UINT16_BE(id, p, 0);
    request_set_length(req, 2);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    *data_len = response_get_length(resp);
    if (*data_len) {
        memcpy(data, resp->payload, *data_len);
    }
    return 0;
}

int se_delete_file(uint16_t id) {
    uint8_t command[16] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_DELETE_FILE);
    uint8_t *p = req->payload;
    // id
    PUT_UINT16_BE(id, p, 0);
    request_set_length(req, 2);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_get_file_size(uint16_t id, size_t *size) {
    uint8_t command[16] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GET_FILE_SIZE);
    uint8_t *p = req->payload;
    // id
    PUT_UINT16_BE(id, p, 0);
    request_set_length(req, 2);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 2) {
        return 1;
    }
    *size = GET_UINT16_BE(resp->payload, 0);
    return 0;
}

int se_set_file_access(uint16_t id, uint8_t access) {
    uint8_t command[16] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_SET_FILE_ACCESS);
    uint8_t *p = req->payload;
    // id
    PUT_UINT16_BE(id, p, 0);
    // move over `id`
    p += 2;
    // access
    *p++ = access;
    request_set_length(req, 3);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_random(size_t len, uint8_t *rnd) {
    uint8_t command[16] = {0};
    uint8_t response[1024] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_RANDOM);
    // len[1]
    req->payload[0] = len & 0xFF;
    request_set_length(req, 1);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != len) {
        return 1;
    }
    memcpy(rnd, resp->payload, len);
    return 0;
}

int se_gen_secret(uint16_t fid, size_t len) {
    CHECK_FID(fid);
    uint8_t command[16] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GEN_SECRET);
    // id[2]|len[1]
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    p += 2;
    *p++ = len & 0xFF;
    request_set_length(req, 3);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    return 0;
}

int se_gen_sym_key(uint16_t fid, uint8_t key_type) {
    CHECK_FID(fid);
    uint8_t command[16] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GEN_KEY);
    // id[2]|type[1]
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    p += 2;
    *p++ = key_type;

    request_set_length(req, 3);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_gen_keypair(uint16_t fid, uint8_t key_type) {
    CHECK_FID(fid);
    uint8_t command[16] = {0};
    uint8_t response[128] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GEN_KEY_PAIR);
    // id[2]|type[1]
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    p += 2;
    *p++ = key_type;
    request_set_length(req, 3);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_get_pubkey(uint16_t fid, uint8_t *pk, size_t *pk_len) {
    CHECK_FID(fid);
    uint8_t command[16] = {0};
    uint8_t response[128] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GET_PUB_KEY);
    // id[2]
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    request_set_length(req, 2);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 65) {
        return 1;
    }
    *pk_len = response_get_length(resp);
    memcpy(pk, resp->payload, *pk_len);
    return 0;
}

int se_cmac(uint16_t fid, const uint8_t *msg, size_t msg_len, uint8_t *cmac) {
    CHECK_FID(fid);
    uint8_t command[1024] = {0};
    uint8_t response[64] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_CMAC);
    // id[2]|mode[1]|len[2]|data
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    p += 2;
    // mode
    *p++ = 0;
    // len
    PUT_UINT16_BE(msg_len, p, 0);
    // move over `len`
    p += 2;
    memcpy(p, msg, msg_len);
    request_set_length(req, 5 + msg_len);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 16) {
        return 1;
    }
    memcpy(cmac, resp->payload, response_get_length(resp));
    return 0;
}

int se_hmac(uint16_t fid, const uint8_t *msg, size_t msg_len, uint8_t *hmac) {
    CHECK_FID(fid);
    uint8_t command[1024] = {0};
    uint8_t response[64] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_HMAC);
    // id[2]|mode[1]|len[2]|data
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    // move over `fid`
    p += 2;
    // mode
    *p++ = 0;
    // len
    PUT_UINT16_BE(msg_len, p, 0);
    // move over `len`
    p += 2;
    memcpy(p, msg, msg_len);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    // the sha256_hamc
    if (response_get_length(resp) != 32) {
        return 1;
    }
    memcpy(hmac, resp->payload, response_get_length(resp));
    return 0;
}

int se_ecdh(uint16_t fid, const uint8_t *pk, size_t pk_len, uint8_t *secret) {
    CHECK_FID(fid);
    uint8_t command[128] = {0};
    uint8_t response[128] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_ECDH);
    // id[2]|<uncompressed public key>
    uint8_t *p = req->payload;
    PUT_UINT16_BE(fid, p, 0);
    // move over `fid`
    p += 2;
    memcpy(p, pk, pk_len);
    request_set_length(req, 2 + pk_len);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 32) {
        return 1;
    }
    memcpy(secret, resp->payload, response_get_length(resp));
    return 0;
}

int se_get_dev_pubkey(uint8_t pubkey[65]) {
    // if (PCB_IS_V1_0()) {
    //     return pcbv10_se_get_pubkey(pubkey) ? 0:1;
    // }
    uint8_t command[3] = {0};
    uint8_t response[128] = { 0 };
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_DEV_PUBKEY);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 65) {
        return 1;
    }

    memcpy(pubkey, resp->payload, response_get_length(resp));
    return 0;
}


int se_get_certificate_len(size_t *cert_len) {
    if (PCB_IS_V1_0()) {
        return pcbv10_se_get_certificate_len(cert_len) ? 0:1;
    }
    *cert_len = 0;
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_DEV_CERT_LENGTH);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 2) {
        return 1;
    }
    *cert_len = GET_UINT16_BE(resp->payload, 0);
    return 0;
}

int se_read_certificate(uint8_t *cert, size_t *cert_len) {
    if (PCB_IS_V1_0()) {
        return pcbv10_se_read_certificate(cert, cert_len) ? 0:1;
    }
    uint8_t command[3] = {0};
    uint8_t response[1024] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_GET_DEV_CERT);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (*cert_len < response_get_length(resp)) {
        return 1;
    }
    *cert_len = response_get_length(resp);
    memcpy(cert, resp->payload, *cert_len);
    return 0;
}

int se_sign_message(uint8_t *msg, size_t msg_len, uint8_t *signature) {
    if (PCB_IS_V1_0()) {
        return pcbv10_se_sign_message(msg, msg_len, signature) ? 0:1;
    }
    uint8_t command[1024] = {0};
    uint8_t response[128] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_DEV_SIGN);
    REQ_PAYLOAD(req, msg, msg_len);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 64) {
        return 1;
    }
    *signature = response_get_length(resp);
    memcpy(signature, resp->payload, response_get_length(resp));
    return 0;
}

int se_verify_app(void) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_VERIFY_APP);
    REQ_EMPTY_PAYLOAD(req);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    // we use 0 as success
    return *resp->payload == 1? 0: 1;
}

int se_install_app(size_t index, const uint8_t* block, size_t block_size) {
    uint8_t command[1024] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);
    REQ_INIT_CMD(command, CMD_ID_INSTALL_APP);
    struct {
        uint8_t block_index_bytes[2];
        // 512 or <512 when is last block
        uint8_t block_size_bytes[2];
        uint8_t data[0];
    } *app_block = (void*)req->payload;
    PUT_UINT16_BE(index, app_block->block_index_bytes, 0);
    PUT_UINT16_BE(block_size, app_block->block_size_bytes, 0);
    memcpy(app_block->data, block, block_size);
    request_set_length(req, block_size + 4);
    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_ping(void) {
    return thd89_ping();
}

int se_has_pin(bool* exist) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_HAS_PIN);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 1) {
        return 1;
    }
    *exist = !!resp->payload[0];
    return 0;
}

int se_set_pin(const uint8_t *pin, size_t pin_len) {
    if (pin_len > 255 || pin_len == 0) {
        return 1;
    }

    uint8_t command[260] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_SET_PIN);
    REQ_PAYLOAD(req, pin, pin_len);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_verify_pin(const uint8_t* pin, size_t pin_len) {
    if (pin_len > 255 || pin_len == 0) {
        return 1;
    }
    uint8_t command[260] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_VERIFY_PIN);
    REQ_PAYLOAD(req, pin, pin_len);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_change_pin(const uint8_t *old_pin, size_t old_pin_len, const uint8_t *new_pin, size_t new_pin_len) {
    if (old_pin_len > 255 || old_pin_len == 0 || new_pin_len > 255 || new_pin_len == 0) {
        return 1;
    }
    uint8_t command[520] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_CHANGE_PIN);
    request_set_length(req, old_pin_len + new_pin_len + 6);
    uint8_t *p = req->payload;
    // old pin
    // move over `tag`
    *p++ = CMD_PARAM_OLD_PIN;
    PUT_UINT16_BE(old_pin_len, p, 0);
    // move over `len`
    p += 2;
    memcpy(p, old_pin, old_pin_len);
    // move over `data`
    p += old_pin_len;


    // new pin
    // move over `tag`
    *p++ = CMD_PARAM_NEW_PIN;
    PUT_UINT16_BE(new_pin_len, p, 0);
    // move over `len`
    p += 2;
    memcpy(p, new_pin, new_pin_len);
    p += new_pin_len;

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    return 0;
}

int se_forget_pin(void) {
    return se_sample_command(CMD_ID_FORGET_PIN);
}

int se_get_pin_max_retry(int *max_retry) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_PIN_MAX_RETRY);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 1) {
        return 1;
    }
    *max_retry = resp->payload[0];
    return 0;
}

int se_get_pin_retry(int *retry) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = sizeof(response);

    REQ_INIT_CMD(command, CMD_ID_GET_PIN_RETRY);
    REQ_EMPTY_PAYLOAD(req);

    int ret = se_execute_command(command, response, &response_size);
    CHECK_CMD_RESULT(ret);
    RESP_INIT(response);
    if (response_get_length(resp) != 1) {
        return 1;
    }
    *retry = resp->payload[0];
    return 0;
}

int se_reset_pin(void) {
    return se_sample_command(CMD_ID_RESET_PIN);
}

bool se_check_app_binary(const uint8_t *binary, size_t binary_len) {
    if (binary_len < 512) return false;
    typedef struct {
        uint8_t magic[4];
        uint32_t version;
        // the `header_t`
        uint32_t header_size;
        // code size
        uint32_t code_size;
        uint8_t digest[32];
        uint8_t signature[64];
    }__attribute__((packed, aligned(512))) header_t ;
    header_t *header = (header_t*)binary;
    if (binary_len != header->header_size + header->code_size) {
        return false;
    }
    uint8_t digest[32] = {0};
    sha256_Raw(binary + header->header_size, header->code_size, digest);
    return memcmp(header->digest, digest, 32) == 0;
}
void se_binary_version(const uint8_t *binary, char version[17]) {
    struct {
        uint8_t build;
        uint8_t patch;
        uint8_t minor;
        uint8_t major;
    } *v = (void*)(binary+4);
    sprintf(version, "%d.%d.%d", v->major, v->minor, v->patch);
    return ;
}

void se_init(void) {
    se_spi_init();
    thd89_init();
    // reset thd89 connection
    thd89_reset();
}

void se_conn_reset(void) {
    thd89_init();
    // reset thd89 connection
    thd89_reset();
}


/// pcb v1.0 device cert
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
#include "string.h"
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
bool pcbv10_se_get_pubkey(uint8_t pubkey[65]) {
    se_obj_t *obj = (se_obj_t *)se_storage_pk_ptr();
    if (memcmp(obj->tag, "PK", 2) != 0) {
        return false;
    }
    memcpy(pubkey, obj->data, 65);
    return true;
}

bool pcbv10_se_get_certificate_len(size_t *cert_len) {
    *cert_len = 0;
    se_obj_t *obj = (se_obj_t *)se_storage_cert_ptr();
    if (memcmp(obj->tag, "CERT", 4) != 0) {
        return false;
    }
    *cert_len = obj->length;
    return true;
}

bool pcbv10_se_read_certificate(uint8_t *cert, size_t *cert_len) {
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

bool pcbv10_se_sign_message(uint8_t *msg, size_t msg_len, uint8_t *signature) {
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
/// pcb v1.0 end

#include "ecdsa.h"
#include "nist256p1.h"
void se_test(void) {
    se_init();

    int ret = se_verify_app();
    printf("verify app: 0x%02x \n", ret);

    // 0. 获取设备状态
    se_state_t state;
    if (!se_get_running_state(&state)) {
        if (state == 0) {
            printf("bootloader\n");
        } else if (state == 1) {
            printf("app\n");
        } else {
            printf("unknown\n");
        }
    } else {
        printf("get state failed\n");
    }

    // 0. 获取生产状态
    life_cycle_t life_cycle;
    if (!se_get_life_cycle(&life_cycle)) {
        if (life_cycle == 0) {
            printf("factory\n");
        } else if (life_cycle == 1) {
            printf("user\n");
        } else {
            printf("unknown\n");
        }
    } else {
        printf("get life cycle failed\n");
    }

    // 1. 擦除设备信息
    if (!se_erase_storage()) {
        printf("erase storage success\n");
    } else {
        printf("erase storage failed\n");
    }

    // need reboot after erase device
    se_reboot();
    // delay a moment wait se start up
    HAL_Delay(50);
    se_conn_reset();

    // 2. 设置序列号
    char *sn = "DS202505170001";
    if (!se_set_sn((uint8_t*)sn, strlen(sn))) {
        printf("set sn success\n");
    } else {
        printf("set sn failed\n");
    }

    // 3. 绑定密钥
    uint8_t key[] = {
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
    };
    if (!se_set_sheared_key(key, sizeof(key))) {
        printf("set sheared key success\n");
    } else {
        printf("set sheared key failed\n");
    }

    // 4. 生成设备密钥
    if (!se_gen_dev_keypair()) {
        printf("gen dev keypair success\n");
    } else {
        printf("gen dev keypair failed\n");
    }

    // 5. 写入设备证书
    uint8_t cert[0x201] = {0x11};
    if (!se_write_certificate(cert, sizeof(cert))) {
        printf("write certificate success\n");
    } else {
        printf("write certificate failed\n");
    }

    // 6. 切换生命周期
    if (!se_switch_life_cycle()) {
        printf("switch life cycle success\n");
    } else {
        printf("switch life cycle failed\n");
    }
    extern void log_data(uint8_t* data, size_t data_size);
    // reboot for switch to user command list
    se_reboot();
    // delay a moment wait se start up
    HAL_Delay(50);
    se_conn_reset();

    // pin test
    bool exist = false;
    if (!se_has_pin(&exist)) {
        printf("has pin: %d\n", exist);
    } else {
        printf("has pin failed\n");
    }

    #define PIN_LEN 4
    uint8_t pin[PIN_LEN] = {'1', '2', '3', '4'};
    if (!se_set_pin(pin, PIN_LEN)) {
        printf("set pin success\n");
    } else {
        printf("set pin failed\n");
    }
    if (!se_has_pin(&exist)) {
        printf("has pin: %d\n", exist);
    } else {
        printf("has pin failed\n");
    }
    ret = se_verify_pin(pin, PIN_LEN);
    if (!ret) {
        printf("verify pin success\n");
    } else {
        printf("verify pin failed: %x\n", ret);
    }
    int retry = 0;
    if (!se_get_pin_retry(&retry)) {
        printf("pin retry: %d\n", retry);
    } else {
        printf("get pin retry failed\n");
    }
    // verify failed
    uint8_t pin2[PIN_LEN] = {'1', '2', '3', '5'};
    ret = se_verify_pin(pin2, PIN_LEN);
    if (!ret) {
        printf("verify pin success\n");
    } else {
        printf("verify pin failed: %x\n", ret);
    }
    if (!se_get_pin_retry(&retry)) {
        printf("pin retry: %d\n", retry);
    } else {
        printf("get pin retry failed\n");
    }

    uint8_t pin3[PIN_LEN] = {'4', '3', '2', '1'};
    if (!se_change_pin(pin, PIN_LEN, pin3, PIN_LEN)) {
        printf("change pin success\n");
    } else {
        printf("change pin failed\n");
    }

    // reset pin can do when pin locked or verified
    // change pin success will make device verified
    if (!se_reset_pin()) {
        printf("reset pin success\n");
    } else {
        printf("reset pin failed\n");
    }
    if (!se_has_pin(&exist)) {
        printf("has pin: %d\n", exist);
    } else {
        printf("has pin failed\n");
    }

    // set a pin for file test
    if (!se_set_pin(pin, PIN_LEN)) {
        printf("set pin success\n");
    } else {
        printf("set pin failed\n");
    }
    se_forget_pin();

    uint8_t __data__[] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38};
    uint16_t __id__ = OID_USER_OBJ_BASE + 0;
    if (!se_write_file(__id__, __data__, sizeof(__data__))) {
        printf("write file success\n");
    } else {
        printf("write file failed\n");
    }

    // the default access is public

    size_t __data_size__ = 0;
    if (!se_get_file_size(__id__, &__data_size__) && __data_size__ == sizeof(__data__)) {
        printf("get file size success\n");
    } else {
        printf("get file size failed\n");
    }

    uint8_t __data2__[8] = {0};
    size_t __data2_size__ = 0;
    if (!se_read_file(__id__, __data2__, &__data2_size__)) {
        printf("read file success\n");
    } else {
        printf("read file failed\n");
    }
    if (__data2_size__ != __data_size__ || memcmp(__data2__, __data__, __data_size__) != 0) {
        printf("read file data error\n");
    }

    // set access to private
    if (!se_set_file_access(__id__, 0)) {
        printf("set file access success\n");
    } else {
        printf("set file access failed\n");
    }

    // can't delete, because have write access
    printf("can't delete file, because have write access\n");
    if (!se_delete_file(__id__)) {
        printf("delete file success\n");
    } else {
        printf("delete file failed\n");
    }

    // verify user pin
    ret = se_verify_pin(pin, PIN_LEN);
    if (!ret) {
        printf("verify pin success\n");
    } else {
        printf("verify pin failed: %x\n", ret);
    }

    // now can delete file
    printf("now can delete file, because have verify pin\n");
    if (!se_delete_file(__id__)) {
        printf("delete file success\n");
    } else {
        printf("delete file failed\n");
    }

    // pin have verified we can wipe user storeage
    if (!se_wipe_user_storage()) {
        printf("wipe user storage success\n");
    } else {
        printf("wipe user storage failed\n");
    }
    while (1) {
        HAL_Delay(1000);
        char version[17] = {0};
        if (!se_get_version(version)) {
            printf("version: %s\n", version);
        } else {
            printf("get version failed\n");
        }

        char sn[33] = {0};
        if (!se_get_sn(sn)) {
            printf("sn: %s\n", sn);
        } else {
            printf("get sn failed\n");
        }

        uint8_t pubkey[65] = {0};
        if (!se_get_dev_pubkey(pubkey)) {
            printf("pubkey: \n");
            log_data(pubkey, sizeof(pubkey));
        } else {
            printf("get pubkey failed\n");
        }

        uint8_t cert[0x201] = {0};
        size_t cert_len = 0;
        if (!se_get_certificate_len(&cert_len)) {
            printf("cert len: %d\n", cert_len);
        } else {
            printf("get cert len failed\n");
        }
        if (!se_read_certificate(cert, &cert_len)) {
            printf("read certificate success\n");
        } else {
            printf("read certificate failed\n");
        }

        char* msg = "1234567890ABCDEF";
        uint8_t sig[64] = {0};
        if (!se_sign_message((uint8_t*)msg, strlen(msg), sig)) {
            printf("sign message success\n");
        } else {
            printf("sign message failed\n");
        }
        uint8_t digest[32] = {0};
        sha256_Raw((uint8_t*)msg, strlen(msg), digest);
        if (!ecdsa_verify_digest(&nist256p1, pubkey,  sig, digest)) {
            printf("verify success\n");
        } else {
            printf("verify failed\n");
        }
    }

}
