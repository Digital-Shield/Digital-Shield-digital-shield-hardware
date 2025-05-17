#ifndef _SE_THD89_H_
#define _SE_THD89_H_
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

/// life cycle object states
typedef enum {
  LCS_FACTORY = 0,
  LCS_USER = 1,

  LCS_UNKNOWN = 0xFF,
}life_cycle_t;

/// which state runing
typedef enum {
  STATE_BOOTLOADER,
  STATE_APP,
}se_state_t;

void se_init(void);
int se_get_life_cycle(life_cycle_t *life_cycle);
int se_get_version(char version[17]);
int se_get_sn(char serial[33]);
int se_get_running_state(se_state_t *state);
int se_reboot_to(se_state_t state);

int se_get_dev_pubkey(uint8_t pubkey[65]);
int se_get_certificate_len(size_t *cert_len);
int se_read_certificate(uint8_t *cert, size_t *cert_len);
int se_sign_message(uint8_t *msg, size_t msg_len, uint8_t *signature);

// se factory function
int se_erase_storage(void);
int se_switch_life_cycle(void);
int se_set_sn(const uint8_t *sn, size_t sn_len);
int se_set_sheared_key(const uint8_t *key, size_t key_len);
int se_gen_dev_keypair(void);
int se_write_certificate(const uint8_t *cert, size_t cert_len);


// helper function
static inline bool se_is_running_bootloader(void) {
  se_state_t state;
  if (0 != se_get_running_state(&state)) {
    return false;
  }
  return state == STATE_BOOTLOADER;
}
static inline bool se_is_running_app(void) {
  se_state_t state;
  if (0 != se_get_running_state(&state)) {
    return false;
  }
  return state == STATE_APP;
}

#endif
