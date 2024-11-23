################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/Components/stmpe811/stmpe811.c 

OBJS += \
./Drivers/Components/stmpe811/stmpe811.o 

C_DEPS += \
./Drivers/Components/stmpe811/stmpe811.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/Components/stmpe811/%.o Drivers/Components/stmpe811/%.su Drivers/Components/stmpe811/%.cyclo: ../Drivers/Components/stmpe811/%.c Drivers/Components/stmpe811/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4S5xx -c -I../Core/Inc -I"C:/Users/nh_14/STM32CubeIDE/workspace_1.16.0/tremor-detector/Drivers/Components" -I"C:/Users/nh_14/STM32CubeIDE/workspace_1.16.0/tremor-detector/Drivers/Components/Common" -I"C:/Users/nh_14/STM32CubeIDE/workspace_1.16.0/tremor-detector/Drivers/Components/lsm6dsl" -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-Components-2f-stmpe811

clean-Drivers-2f-Components-2f-stmpe811:
	-$(RM) ./Drivers/Components/stmpe811/stmpe811.cyclo ./Drivers/Components/stmpe811/stmpe811.d ./Drivers/Components/stmpe811/stmpe811.o ./Drivers/Components/stmpe811/stmpe811.su

.PHONY: clean-Drivers-2f-Components-2f-stmpe811
