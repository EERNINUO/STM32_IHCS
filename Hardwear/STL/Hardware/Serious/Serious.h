#ifndef __SERIAL_H
#define __SERIAL_H

#ifdef __cplusplus
 extern "C"{
#endif

#include "stm32f10x.h"

void Serial_init(void);
void Serial_send_ushort(uint16_t dat);
void Serial_send_float(float dat);
void Serial_send_arr(uint8_t* dat);

#ifdef __cplusplus
 }
#endif

#endif