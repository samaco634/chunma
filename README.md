python selenium_with_thread_and_libgpiod.py  

-----------------------------
# chunma
https://www.acmesystems.it/rotary_encoder

1안 

chmod +x orangepi_encoder.sh

orangepi_encoder.sh

orangepi_encoder.py

orangepi_with_gpio_interrupt.py


2안 

device tree overlay

gpio-rotary.dts or gpio-rotary2.dts

selenium_with_thread_and_endev.py

encoder_evdev_class.py 


3안

sudo apt update

sudo apt install gpiod

sudo gpiodetect

sudo gpioinfo fc038000.pinctrl #gpiodetect 의 결과

sudo gpiofind "PD4"

sudo gpiofind "PC4"

sudo gpioget gpiochip0 0 # gpiofind의 결과


sudo apt update

sudo apt install python3-libgpiod


test_libgpiod.py

test_libgpiod2.py

sudo필요한지 여부 확인


