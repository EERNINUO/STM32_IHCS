/*******************************************************************************
* GNU GENERAL PUBLIC LICENSE (GPL) v3.0
*
* Copyright (c) EERNIINUO
* which is available at https://github.com/EERNINUO/STM32_IHCS
* All rights reserved.
*
********************************************************************************/

#include "stm32f10x.h"                  // Device header
#include "DHT11.h"
#include "Serious.h"
#include "JQ01.h"
#include "PRC905.h"
#include "OLED.h"
#include "timer.h"

extern uint8_t dat_arr[6];

int main(void){
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	Serial_init();
	DHT11_Init();
	JQ01_Init();
	PRC905_init();
	timer_init();
	while(1){
		;
	}
}
