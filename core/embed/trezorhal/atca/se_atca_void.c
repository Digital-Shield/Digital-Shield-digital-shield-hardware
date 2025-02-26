#include "se_atca.h"
char *se_get_version(void){
    return "1.0.0";
}
bool se_get_sn(char **serial){
    (void)serial;
    return false;
}

bool se_setSeedStrength(uint32_t strength){
    (void)strength;
    return false;
}
bool se_getSeedStrength(uint32_t *strength){
    (void)strength;
    return false;
}
bool se_importSeed(uint8_t *seed){
    (void)seed;
    return false;
}
bool se_export_seed(uint8_t *seed){
    (void)seed;
    return false;
}
void se_get_status(void){
    return;
}
bool se_hasPin(void){
    return false;
}
bool se_verifyPin(const char *pin){
    (void)pin;
    return false;
}
bool se_setPin(const char *pin){
    (void)pin;
    return false;
}
bool se_changePin(const char *old_pin, const char *new_pin){
    (void)old_pin;
    (void)new_pin;
    return false;
}
bool se_reset_pin(void){
    return false;
}
bool se_isInitialized(void){
    return false;
}
bool se_is_wiping(void){
    return false;
}
void se_set_wiping(bool flag){
    (void)flag;
    return;
}
void se_reset_state(void){
    return;
}
void se_reset_storage(void){
    return;
}
uint32_t se_pinFailedCounter(void){
    return 0;
}
bool se_device_init(uint8_t mode, const char *passphrase){
    (void)mode;
    (void)passphrase;
    return false;
}

bool se_get_pubkey(uint8_t pubkey[64]){
    (void)pubkey;
    return false;
}
bool se_write_certificate(const uint8_t *cert, uint32_t cert_len){
    (void)cert;
    (void)cert_len;
    return false;
}
bool se_get_certificate_len(uint32_t *cert_len){
    (void)cert_len;
    return false;
}
bool se_read_certificate(uint8_t *cert, uint32_t *cert_len){
    (void)cert;
    (void)cert_len;
    return false;
}
bool se_sign_message(uint8_t *msg, uint32_t msg_len, uint8_t *signature){
    (void)msg;
    (void)msg_len;
    (void)signature;
    return false;
}
void se_init(void)  {
    return;
}

void fake_func(func_pointer func_p){
    (void)func_p;
    return;
}