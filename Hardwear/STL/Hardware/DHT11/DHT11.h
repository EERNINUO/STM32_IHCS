#ifndef __DHT11_H
#define __DHT11_H

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

// #define STM32F10X_MD

#include "stm32f10x.h"
#include "Delay.h"
#include "Serious.h"

void DHT11_Init(void);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // __DHT11_H