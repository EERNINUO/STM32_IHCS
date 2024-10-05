#include "Serious.h"

extern uint8_t dat_arr[5];

void Serial_init(){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);
    // RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE);

    GPIO_InitTypeDef Serial_gpio_init;
    Serial_gpio_init.GPIO_Mode = GPIO_Mode_AF_PP;
    Serial_gpio_init.GPIO_Pin = GPIO_Pin_9;
    Serial_gpio_init.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA,&Serial_gpio_init);

    USART_InitTypeDef Serial_usart_init;
    Serial_usart_init.USART_BaudRate = 115200;
    Serial_usart_init.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    Serial_usart_init.USART_Mode = USART_Mode_Tx;
    Serial_usart_init.USART_Parity = USART_Parity_No;
    Serial_usart_init.USART_StopBits = USART_StopBits_1;
    Serial_usart_init.USART_WordLength = USART_WordLength_8b;
    USART_Init(USART1,&Serial_usart_init);

    // DMA_InitTypeDef DHT11_dma_init;
    // DHT11_dma_init.DMA_MemoryBaseAddr = (uint32_t)dat_arr;
    // DHT11_dma_init.DMA_MemoryDataSize = DMA_MemoryDataSize_Byte;
    // DHT11_dma_init.DMA_MemoryInc = DMA_MemoryInc_Enable;
    // DHT11_dma_init.DMA_PeripheralBaseAddr = (uint32_t)&USART1->DR;
    // DHT11_dma_init.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Byte;
    // DHT11_dma_init.DMA_PeripheralInc = DMA_PeripheralInc_Disable;
    // DHT11_dma_init.DMA_BufferSize = 4;
    // DHT11_dma_init.DMA_DIR = DMA_DIR_PeripheralDST;
    // DHT11_dma_init.DMA_M2M = DMA_M2M_Disable;
    // DHT11_dma_init.DMA_Mode = DMA_Mode_Normal;
    // DHT11_dma_init.DMA_Priority = DMA_Priority_Medium;
    // DMA_Init(DMA1_Channel4,&DHT11_dma_init);

    // NVIC_InitTypeDef Serial_nvic_init;
    // Serial_nvic_init.NVIC_IRQChannel = DMA1_Channel4_IRQn;
    // Serial_nvic_init.NVIC_IRQChannelCmd = ENABLE;
    // Serial_nvic_init.NVIC_IRQChannelPreemptionPriority = 0;
    // Serial_nvic_init.NVIC_IRQChannelSubPriority = 0;
    // NVIC_Init(&Serial_nvic_init);

    // DMA_ITConfig(DMA1_Channel4, DMA_IT_TC, ENABLE);
    // USART_DMACmd(USART1, USART_DMAReq_Tx, ENABLE);
    USART_Cmd(USART1,ENABLE);
}

void Serial_send_float(float dat){
    uint8_t* u8_dat = &dat;
    for (uint8_t i = 0; i<4; i++){
        USART_SendData(USART1,u8_dat[i]);
        while (USART_GetFlagStatus (USART1, USART_FLAG_TXE) == RESET);
    }
}

void Serial_send_ushort(uint16_t dat){
    uint8_t* u8_dat = &dat;
    USART_SendData(USART1,u8_dat[0]);
    while (USART_GetFlagStatus (USART1, USART_FLAG_TXE) == RESET);
    USART_SendData(USART1,u8_dat[1]);
    while (USART_GetFlagStatus (USART1, USART_FLAG_TXE) == RESET);
}

void Serial_send_arr(uint8_t *dat){
    for (uint8_t i = 0; i<6; i++){
        USART_SendData(USART1,dat[i]);
        while (USART_GetFlagStatus (USART1, USART_FLAG_TXE) == RESET);
    }
}

// void DMA1_Channel4_IRQHandler(void){
//     DMA_Cmd(DMA1_Channel4, DISABLE);
//     DMA_ClearITPendingBit(DMA1_IT_TC4);
// }