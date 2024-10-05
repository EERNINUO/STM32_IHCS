#include "timer.h"

uint8_t dat_arr[6];

void timer_init(){
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    TIM_TimeBaseInitTypeDef DHT11_tb_init;
    DHT11_tb_init.TIM_ClockDivision = TIM_CKD_DIV1;
    DHT11_tb_init.TIM_CounterMode = TIM_CounterMode_Up;
    DHT11_tb_init.TIM_Period = 1000 - 1;
    DHT11_tb_init.TIM_Prescaler = 7200 - 1;
    DHT11_tb_init.TIM_RepetitionCounter = 0;
    TIM_TimeBaseInit(TIM2, &DHT11_tb_init);

    TIM_ClearFlag(TIM2, TIM_FLAG_Update);

    NVIC_InitTypeDef DHT11_nvic_init;
    DHT11_nvic_init.NVIC_IRQChannel = TIM2_IRQn;
    DHT11_nvic_init.NVIC_IRQChannelCmd = ENABLE;
    DHT11_nvic_init.NVIC_IRQChannelPreemptionPriority = 0;
    DHT11_nvic_init.NVIC_IRQChannelSubPriority = 0;
    NVIC_Init(&DHT11_nvic_init);

    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
    TIM_Cmd(TIM2, ENABLE);
}

void TIM2_IRQHandler(void){
    DHT11_read(dat_arr);
    PRC905_read(dat_arr);
    // DMA_reset();
    // DMA_Cmd(DMA1_Channel4, DISABLE);
    // DMA_SetCurrDataCounter(DMA1_Channel4, 4);
    // DMA_Cmd(DMA1_Channel4, ENABLE);
    TIM_ClearITPendingBit(TIM2, TIM_IT_Update); 
    Serial_send_arr(dat_arr);
}
