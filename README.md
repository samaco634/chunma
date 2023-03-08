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

---  
root@imx8mm-cgt-sx8m: cat /sys/kernel/debug/gpio  
gpiochip0: GPIOs 0-31, parent: platform/30200000.gpio, 30200000.gpio:  
gpio-1 ( |bkl pwm ) out hi  
gpio-8 ( |enable ) out hi  
gpio-9 ( |rotary@0 ) in lo IRQ ACTIVE LOW  
gpio-10 ( |rotary@0 ) in lo IRQ  
gpio-12 ( |regulator-usb ) out lo  
---  
root@imx8mm-cgt-sx8m:~# cat /proc/interrupts    

.  

.  

73: 0 gpio-mxc 9 Edge rotary-encoder  
74: 0 gpio-mxc 10 Edge rotary-encoder  
----  
root@imx8mm-cgt-sx8m:~# evtest  
No device specified, trying to scan all of /dev/input/event*  
Available devices:  
/dev/input/event0: 30370000.snvs:snvs-powerkey  
/dev/input/event1: rotary@0  
/dev/input/event2: gpio-keys  
/dev/input/event3: bd718xx-pwrkey  
/dev/input/event4: PixArt Dell MS116 USB Optical Mouse  
Select the device event number [0-4]: 1  
Input driver version is 1.0.1  
Input device ID: bus 0x19 vendor 0x0 product 0x0 version 0x0  
Input device name: "rotary@0"  
Supported events:  
Event type 0 (EV_SYN)  
Event type 2 (EV_REL)  
Event code 1 (REL_Y)  
Properties:  
Testing ... (interrupt to exit)  
-------
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


