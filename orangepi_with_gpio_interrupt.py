# https://www.ics.com/blog/gpio-programming-using-sysfs-interface
# $ echo 92 >/sys/class/gpio/export (physical 22)
# $ echo 52 >/sys/class/gpio/export (physical 24)
# $ ls /sys/class/gpio
# $ ls /sys/class/gpio/gpio92/
# $ ls /sys/class/gpio/gpio52/
# $ echo in >/sys/class/gpio/gpio92/direction
# $ echo in >/sys/class/gpio/gpio52/direction

#The final step, if you are finished using the GPIO pin, is to unexport it. To do this, just write the pin name to the unexport file, i.e.
# $ echo 92 >/sys/class/gpio/unexport
# $ echo 52 >/sys/class/gpio/unexport

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
from qr_read import readQRCode

import RPi.GPIO as GPIO
from encoder_orangepi import Encoder

option = Options()
option.add_argument("--start-maximized")
option.add_argument("--no-sandbox")
option.add_argument("--disable-web-security")
option.add_argument("--ignore-certificate-errors")
option.add_argument("--kiosk")
option.add_argument("--disable-password-manager-reauthentication")
option.add_argument("--disable-infobars")
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=option)
driver.get("https://www.naver.com")

currentPosition = 0
def valueChanged(value, direction):
    global driver
    global currentPosition
    print("* New value: {}, Direction: {}".format(value, direction))
    if(direction == 'L'):
        currentPosition -= 100
        if(currentPosition < 0):
            currentPosition = 0
    elif(direction == 'R'):
        currentPosition += 100
    driver.execute_script("window.scrollTo(0, "+str(currentPosition)+")")

e1 = Encoder(92, 52, valueChanged)

# Default size
print(driver.get_window_size())

try:
    while True:
      url = readQRCode()
      driver.get(url)
      currentPosition = 0

except Exception:
    pass

GPIO.cleanup()
