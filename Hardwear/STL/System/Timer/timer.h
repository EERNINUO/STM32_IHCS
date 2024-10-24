#ifndef __TIMER_H
#define __TIMER_H

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

#include "stm32f10x.h"
#include "DHT11.h"
#include "PRC905.h"

void timer_init(void);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // __TIMER_H