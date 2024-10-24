#include "DHT11.h"

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

    GPIO_InitTypeDef DHT11_gpio_init;
    DHT11_gpio_init.GPIO_Mode = GPIO_Mode_Out_OD;
    DHT11_gpio_init.GPIO_Pin = GPIO_Pin_14;
    DHT11_gpio_init.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &DHT11_gpio_init);
}

void DHT11_read(uint8_t* dat_arr){
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
    while (!data_read());
}