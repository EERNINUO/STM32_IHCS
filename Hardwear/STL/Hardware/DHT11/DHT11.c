#include "DHT11.h"

uint8_t dat_arr[5];

#define data_write(num) GPIO_WriteBit(GPIOB, GPIO_Pin_14, (BitAction)(num))
#define data_read() GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_14)

void DHT11_Reset(void){
    data_write(0);
    Delay_us(20);
    data_write(1);
    while (data_read());
    while (!data_read());
	while (data_read());
}

void DHT11_Init(void){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);

    GPIO_InitTypeDef DHT11_gpio_init;
    DHT11_gpio_init.GPIO_Mode = GPIO_Mode_Out_OD;
    DHT11_gpio_init.GPIO_Pin = GPIO_Pin_14;
    DHT11_gpio_init.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &DHT11_gpio_init);

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
    DHT11_Reset();
    for (uint8_t i=0; i< 5; i++){
        for (uint8_t j=0; j<8; j++){
            while (!data_read());
            Delay_us(40);
            dat_arr[i] <<= 1;
            if (data_read() == 1){ 
                dat_arr[i] += 1;
                while (data_read() == 1);
            }
        }
    }
    while (!data_read())
    // DMA_reset();
    // DMA_Cmd(DMA1_Channel4, DISABLE);
    // DMA_SetCurrDataCounter(DMA1_Channel4, 4);
    // DMA_Cmd(DMA1_Channel4, ENABLE);
    TIM_ClearITPendingBit(TIM2, TIM_IT_Update); 
    Serial_send_arr(dat_arr);
}
