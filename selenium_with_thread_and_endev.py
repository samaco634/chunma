from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
from qr_read import readQRCode
from encoder_endev import Encoder
import threading

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


# Default size
print(driver.get_window_size())

env = EncoderEvdev (valueChanged);
my_thread = threading.Thread(target=env.run)
my_thread.start()

try:
    while True:
      url = readQRCode()
      driver.get(url)
      currentPosition = 0

except Exception:
    pass
