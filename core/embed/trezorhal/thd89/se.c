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

  // 管理指令
  CMD_ID_REBOOT = 0x10,
};

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

static inline size_t command_size(const request_t* req) {
  return 3 + request_get_length(req);
}

typedef enum {
  RESP_CODE_SUCCESS = 0,
  RESP_CODE_INTERNAL_FAILED,
  RESP_CODE_INVALID_STATE,
  RESP_CODE_INVALID_PARAM_DATA,
  RESP_CODE_UNSUPPORTED_COMMAND,
  RESP_CODE_OBJECT_ALREADY_EXIST,
  RESP_CODE_OBJECT_NOT_EXIST,
} response_code_t;

int se_get_version(char version[17]) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_VERSION);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    // command result
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    if (response_get_length(resp) != 4) {
        return 1;
    }
    struct {
        uint8_t major;
        uint8_t minor;
        uint8_t patch;
        uint8_t build;
    } *v = (void*)resp->payload;
    sprintf(version, "%d.%d.%d.%d", v->major, v->minor, v->patch, v->build);
    return 0;
}

int se_get_sn(char serial[33]) {
    uint8_t command[3] = {0};
    uint8_t response[64] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_SN);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    memcpy(serial, resp->payload, response_get_length(resp));
    return 0;
}

int se_get_running_state(se_state_t *state) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_STATE);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    *state = (se_state_t)resp->payload[0];
    return 0;
}

int se_get_life_cycle(life_cycle_t *life_cycle) {
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_LIFE_CYCLE);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    *life_cycle = (life_cycle_t)resp->payload[0];
    return 0;
}

int se_reboot_to(se_state_t state) {
    uint8_t command[4] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_REBOOT);
    REQ_PAYLOAD(req, &state, 1);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    return 0;
}

int se_get_dev_pubkey(uint8_t pubkey[65]) {
    uint8_t command[3] = {0};
    uint8_t response[128] = { 0 };
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_DEV_PUBKEY);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    if (response_get_length(resp) != 65) {
        return 1;
    }

    memcpy(pubkey, resp->payload, response_get_length(resp));
    return 0;
}


int se_get_certificate_len(size_t *cert_len) {
    *cert_len = 0;
    uint8_t command[3] = {0};
    uint8_t response[16] = {0};
    size_t response_size = 0;

    REQ_INIT_CMD(command, CMD_ID_GET_DEV_CERT_LENGTH);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    if (response_get_length(resp) != 2) {
        return 1;
    }
    *cert_len = GET_UINT16_BE(resp->payload, 0);
    return 0;
}

int se_read_certificate(uint8_t *cert, size_t *cert_len) {
    uint8_t command[3] = {0};
    uint8_t response[1024] = {0};
    size_t response_size = 0;
    REQ_INIT_CMD(command, CMD_ID_GET_DEV_CERT);
    REQ_EMPTY_PAYLOAD(req);

    thd89_result_t ret = thd89_execute_command(command, sizeof(command), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    *cert_len = response_get_length(resp);
    memcpy(cert, resp->payload, *cert_len);
    return 0;
}

int se_sign_message(uint8_t *msg, size_t msg_len, uint8_t *signature) {
    uint8_t command[1024] = {0};
    uint8_t response[128] = {0};
    size_t response_size = 0;
    REQ_INIT_CMD(command, CMD_ID_DEV_SIGN);
    REQ_PAYLOAD(req, msg, msg_len);

    thd89_result_t ret = thd89_execute_command(command, command_size(req), response, sizeof(response), &response_size);
    // transmit result
    if (ret != THD89_SUCCESS) {
        return 1;
    }
    RESP_INIT(response);
    if (resp->code != RESP_CODE_SUCCESS) {
        return 1;
    }
    if (response_get_length(resp) != 64) {
        return 1;
    }
    *signature = response_get_length(resp);
    memcpy(signature, resp->payload, response_get_length(resp));
    return 0;
}

void se_init(void) {
    se_spi_init();
    thd89_init();
    // reset thd89 connection
    thd89_reset();
}

#include "ecdsa.h"
#include "nist256p1.h"
void se_test(void) {
    se_init();

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
