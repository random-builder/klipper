#
#
#

mcu_BASE = "MCU 'mcu' config: ADC_MAX=4095 BUS_PINS_i2c0=P0.28,P0.27 BUS_PINS_i2c1=P0.1,P0.0 BUS_PINS_i2c1a=P0.20,P0.19 BUS_PINS_i2c2=P0.11,P0.10 BUS_PINS_ssp0=P0.17,P0.18,P0.15 BUS_PINS_ssp1=P0.8,P0.9,P0.7 CLOCK_FREQ=100000000 MCU=lpc1768 PWM_MAX=255 RESERVE_PINS_USB=P0.30,P0.29,P2.9 STATS_SUMSQ_BASE=256 STEPPER_BOTH_EDGE=1"
mcu_OCTA = "MCU 'OCTA' config: ADC_MAX=4095 BUS_PINS_i2c1=PB6,PB7 BUS_PINS_i2c1a=PB8,PB9 BUS_PINS_i2c2=PB10,PB11 BUS_PINS_i2c3=PA8,PC9 BUS_PINS_sdio=PC12,PD2,PC8,PC9,PC10,PC11 BUS_PINS_spi1=PA6,PA7,PA5 BUS_PINS_spi1a=PB4,PB5,PB3 BUS_PINS_spi2=PB14,PB15,PB13 BUS_PINS_spi2a=PC2,PC3,PB10 BUS_PINS_spi3=PB4,PB5,PB3 BUS_PINS_spi3a=PC11,PC12,PC10 BUS_PINS_spi4=PE13,PE14,PE12 CLOCK_FREQ=180000000 MCU=stm32f446xx PWM_MAX=255 RESERVE_PINS_USB=PA11,PA12 RESERVE_PINS_crystal=PH0,PH1 STATS_SUMSQ_BASE=256 STEPPER_BOTH_EDGE=1"
mcu_TARA = "MCU 'TARA' config: ADC_MAX=4095 BUS_PINS_i2c1=PB6,PB7 BUS_PINS_i2c1a=PB8,PB9 BUS_PINS_i2c2=PB10,PB11 BUS_PINS_i2c3=PA8,PC9 BUS_PINS_sdio=PC12,PD2,PC8,PC9,PC10,PC11 BUS_PINS_spi1=PA6,PA7,PA5 BUS_PINS_spi1a=PB4,PB5,PB3 BUS_PINS_spi2=PB14,PB15,PB13 BUS_PINS_spi2a=PC2,PC3,PB10 BUS_PINS_spi3=PB4,PB5,PB3 BUS_PINS_spi3a=PC11,PC12,PC10 BUS_PINS_spi4=PE13,PE14,PE12 CLOCK_FREQ=180000000 MCU=stm32f446xx PWM_MAX=255 RESERVE_PINS_USB=PA11,PA12 RESERVE_PINS_crystal=PH0,PH1 STATS_SUMSQ_BASE=256 STEPPER_BOTH_EDGE=1"


def report_mcu_config(mcu_line:str):
    print(f"===========================")
    base_list = mcu_line.split("config:")
    base_name = base_list[0]
    term_list = base_list[1].split(" ")
    print(base_name)
    for term_item in term_list:
        print(term_item)


report_mcu_config(mcu_BASE)
report_mcu_config(mcu_OCTA)
report_mcu_config(mcu_TARA)

#
#
#
