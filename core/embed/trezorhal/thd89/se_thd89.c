#include <stdbool.h>
#include <stdint.h>
#include "se_thd89.h"
#include <stddef.h>

char *se_get_version(void) {
    return NULL;
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

bool se_device_init(uint8_t mode, const char *passphrase) {
    (void)mode; // Prevent unused parameter warning
    (void)passphrase; // Prevent unused parameter warning
    return false;
}

bool se_get_pubkey(uint8_t pubkey[64]) {
    (void)pubkey; // Prevent unused parameter warning
    return false;
}

bool se_write_certificate(const uint8_t *cert, uint32_t cert_len) {
    (void)cert; // Prevent unused parameter warning
    (void)cert_len; // Prevent unused parameter warning
    return false;
}

bool se_get_certificate_len(uint32_t *cert_len) {
    *cert_len = 0;
    return false;
}

bool se_read_certificate(uint8_t *cert, uint32_t *cert_len) {
    (void)cert; // Prevent unused parameter warning
    *cert_len = 0;
    return false;
}

bool se_sign_message(uint8_t *msg, uint32_t msg_len, uint8_t *signature) {
    (void)msg; // Prevent unused parameter warning
    (void)msg_len; // Prevent unused parameter warning
    (void)signature; // Prevent unused parameter warning
    return false;
}

void se_init(void) {
    // Empty implementation
}

