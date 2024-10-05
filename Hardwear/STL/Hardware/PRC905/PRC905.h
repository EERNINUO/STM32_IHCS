#ifndef __PRC905_H
#define __PRC905_H

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

#include "stm32f10x.h"

void PRC905_init(void);
void PRC905_read(uint8_t* dat_arr);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // __PRC905_H