#include "se.h"
#include <stdint.h>

static const uint8_t FIXED_SALT[32] = {
    0xd0, 0xaa, 0x97, 0x03, 0xad, 0xa5, 0x1d, 0xb7, 0x05, 0x47, 0xe7, 0xc8, 0xa2, 0x1e, 0x4c, 0x37,
    0xb1, 0xbb, 0x9e, 0xcf, 0xb8, 0xdb, 0xd6, 0x65, 0x71, 0x0e, 0x9b, 0x47, 0x77, 0x41, 0x63, 0x39
};

static inline void xor(const uint8_t* a, uint8_t* b, size_t n) {
    while(n--) {
        *b++ ^= *a++;
    }
}

int se_verify_user_pin(uint8_t pin[32]) {
    xor(FIXED_SALT, pin, 32);
    return 0;
}

int se_set_user_pin(uint8_t pin[32]) {
    xor(FIXED_SALT, pin, 32);
    return 0;
}

int se_wipe_user_storage(void) {
    return 0;
}

int se_forget_pin(void) {
    return 0;
}