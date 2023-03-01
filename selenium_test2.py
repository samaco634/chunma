from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
from qr_read import readQRCode

import RPi.GPIO as GPIO
from encoder import Encoder

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
state = "00"
direction = "R"
value = 0
def interrupdetected(channel):
    global state
    global direction
    global value
    p1 = GPIO.input(18)
    p2 = GPIO.input(17)
    newState = "{}{}".format(p1, p2)
    print(newState)

    if state == "00": # Resting position
        if newState == "01": # Turned right 1
            direction = "R"
        elif newState == "10": # Turned left 1
            direction = "L"

    elif state == "01": # R1 or L3 position
        if newState == "11": # Turned right 1
            direction = "R"
        elif newState == "00": # Turned left 1
            if direction == "L":
                value = value - 1
                print("* New value: {}, Direction: {}".format(value, direction))
                valueChanged(value, direction)

    elif state == "10": # R3 or L1
        if newState == "11": # Turned left 1
            direction = "L"
        elif newState == "00": # Turned right 1
            if direction == "R":
                value = value + 1
                print("* New value: {}, Direction: {}".format(value, direction))
                valueChanged(value, direction)

    else: # state == "11"
        if newState == "01": # Turned left 1
            direction = "L"
        elif newState == "10": # Turned right 1
            direction = "R"
        elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
            if direction == "L":
                value = value - 1
                print("* New value: {}, Direction: {}".format(value, direction))
                valueChanged(value, direction)
            elif direction == "R":
                value = value + 1
                print("* New value: {}, Direction: {}".format(value, direction))
                valueChanged(value, direction)
            
    state = newState

GPIO.setmode(GPIO.BCM)
#e1 = Encoder(18, 17, valueChanged)
GPIO.setup(18, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(18, GPIO.BOTH, interrupdetected)  
GPIO.add_event_detect(17, GPIO.BOTH, interrupdetected)  


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
