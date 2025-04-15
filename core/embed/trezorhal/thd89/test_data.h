#ifndef __TEST_DATA_H__
#define __TEST_DATA_H__

#define TESTING_MODE 1

#if TESTING_MODE
#include <stdint.h>

extern uint8_t SECRET[32];
extern uint8_t RND[32];
extern uint8_t SSEQ[4];
extern uint8_t KEYS[40];
extern uint8_t MASTER_ENC_KEY[16];
extern uint8_t MASTER_DEC_KEY[16];
extern uint8_t MASTER_ENC_NONCE[4];
extern uint8_t MASTER_DEC_NONCE[4];
extern uint8_t SLAVE_ENC_KEY[16];
extern uint8_t SLAVE_DEC_KEY[16];
extern uint8_t SLAVE_ENC_NONCE[4];
extern uint8_t SLAVE_DEC_NONCE[4];
extern uint8_t HELLO_RESPONSE_PAYLOAD[36];
extern uint8_t MASTER_FINISHED_ENCRYPT_ASSOCIATED[8];
extern uint8_t MASTER_FINISHED_ENCRYPT_NONCE[8];
extern uint8_t MASTER_FINISHED_CIPHERTEXT[44];
extern uint8_t SLAVE_FINISHED_DECRYPT_NONCE[8];
extern uint8_t SLAVE_DECRYPTED_PAYLOAD[36];
extern uint8_t MSEQ[4];
extern uint8_t SLAVE_FINISHED_PAYLOAD[36];
extern uint8_t SLAVE_FINISHED_ENCRYPT_ASSOCIATED[8];
extern uint8_t SLAVE_FINISHED_ENCRYPT_NONCE[8];
extern uint8_t SLAVE_FINISHED_CIPHERTEXT[44];
extern uint8_t MASTER_FINISHED_DECRYPT_NONCE[8];
extern uint8_t MASTER_DECRYPTED_PAYLOAD[36];

#endif

#endif
