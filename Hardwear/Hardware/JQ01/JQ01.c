#include "JQ01.h"

uint8_t warring_arr[4] = {0xAA, 0xAA, 0xAA, 0xAA};
uint8_t warring_end[4] = {0xBB, 0xBB, 0xBB, 0xBB};

void JQ01_Init(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);

    GPIO_InitTypeDef jq01_gpio_init;
    jq01_gpio_init.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    jq01_gpio_init.GPIO_Pin = GPIO_Pin_5;
    jq01_gpio_init.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &jq01_gpio_init);

	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource5);

    EXTI_InitTypeDef jq01_exti_init;
    jq01_exti_init.EXTI_Line = EXTI_Line5;
    jq01_exti_init.EXTI_LineCmd = ENABLE;
    jq01_exti_init.EXTI_Mode = EXTI_Mode_Interrupt;
    jq01_exti_init.EXTI_Trigger = EXTI_Trigger_Rising_Falling;
    EXTI_Init(&jq01_exti_init);

    NVIC_InitTypeDef jq01_nvic_init;
    jq01_nvic_init.NVIC_IRQChannel = EXTI9_5_IRQn;
    jq01_nvic_init.NVIC_IRQChannelCmd = ENABLE;
    jq01_nvic_init.NVIC_IRQChannelPreemptionPriority = 1;
    jq01_nvic_init.NVIC_IRQChannelSubPriority = 1;
    NVIC_Init(&jq01_nvic_init);
}

void EXTI9_5_IRQHandler(){
    if (EXTI_GetITStatus(EXTI_Line5) == SET){
        if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_5) == 1) 
        Serial_send_arr(warring_arr);
        else if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_5) == 0)
            Serial_send_arr(warring_end);
        EXTI_ClearITPendingBit(EXTI_Line5);
    }
}