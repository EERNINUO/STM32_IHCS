#include "PRC905.h"

extern uint8_t dat_arr[10];

void PRC905_init(){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA1, ENABLE);

    GPIO_InitTypeDef prc905_gpio_init;
    prc905_gpio_init.GPIO_Mode = GPIO_Mode_AIN;
    prc905_gpio_init.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2;
    prc905_gpio_init.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &prc905_gpio_init);

    ADC_InitTypeDef prc905_adc_init;
    prc905_adc_init.ADC_ContinuousConvMode = DISABLE;
    prc905_adc_init.ADC_DataAlign = ADC_DataAlign_Right;
    prc905_adc_init.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
    prc905_adc_init.ADC_Mode = ADC_Mode_Independent;
    prc905_adc_init.ADC_NbrOfChannel = 3;
    prc905_adc_init.ADC_ScanConvMode = ENABLE;
    ADC_Init(ADC1, &prc905_adc_init);

    ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_239Cycles5);
    ADC_RegularChannelConfig(ADC1, ADC_Channel_1, 2, ADC_SampleTime_239Cycles5);
    ADC_RegularChannelConfig(ADC1, ADC_Channel_2, 3, ADC_SampleTime_239Cycles5);

    DMA_InitTypeDef adc_dma_init;
    adc_dma_init.DMA_MemoryBaseAddr = (uint32_t)&(dat_arr[4]);
    adc_dma_init.DMA_MemoryDataSize = DMA_MemoryDataSize_HalfWord;
    adc_dma_init.DMA_MemoryInc = DMA_MemoryInc_Enable;
    adc_dma_init.DMA_PeripheralBaseAddr = (uint32_t)&ADC1->DR;
    adc_dma_init.DMA_PeripheralDataSize = DMA_PeripheralDataSize_HalfWord;
    adc_dma_init.DMA_PeripheralInc = DMA_PeripheralInc_Disable;
    adc_dma_init.DMA_BufferSize = 3;
    adc_dma_init.DMA_DIR = DMA_DIR_PeripheralSRC;
    adc_dma_init.DMA_M2M = DMA_M2M_Disable;
    adc_dma_init.DMA_Mode = DMA_Mode_Circular;
    adc_dma_init.DMA_Priority = DMA_Priority_Low;
    DMA_Init(DMA1_Channel1, &adc_dma_init);

    ADC_Cmd(ADC1, ENABLE);
    ADC_DMACmd(ADC1,ENABLE);
    DMA_Cmd(DMA1_Channel1, ENABLE);

    ADC_ResetCalibration(ADC1);
    while (ADC_GetResetCalibrationStatus(ADC1));
    ADC_StartCalibration(ADC1);
    while (ADC_GetCalibrationStatus(ADC1));
}

void PRC905_read(uint8_t* dat_arr){
    ADC_SoftwareStartConvCmd(ADC1, ENABLE);
    while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET);
    uint16_t adc_value = ADC_GetConversionValue(ADC1);
    uint8_t* change = &adc_value;
    dat_arr[4] = change[0];
    dat_arr[5] = change[1];
}