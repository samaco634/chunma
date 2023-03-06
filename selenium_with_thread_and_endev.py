from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
from qr_read import readQRCode
from encoder_evdev_class import EncoderEvdev
import threading

url_list = ["https://www.naver.com/",
            "https://www.youtube.com/",
            "https://www.apple.com/"
            ]

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
window_size_x, window_size_y = driver.get_window_size().values()
# 스크롤 높이 가져옴
max_scroll = driver.execute_script("return document.body.scrollHeight")
#max_scroll = driver.execute_script;("return document.body.scrollWidth")


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
        if(currentPosition > max_scroll):
            currentPosition = max_scroll
    print("current position {}, last_height {}".format(currentPosition, max_scroll))
    driver.execute_script("window.scrollTo(0, "+str(currentPosition)+")") 
    timer = reset_timer(timer)

def timeout():
    raise TimeoutError("Timeout occurred after 3 minutes.")

def reset_timer(timer):
    if timer not 0:
        timer.cancel()
    new_timer = threading.Timer(180, timeout)
    new_timer.daemon = True
    new_timer.start()
    return new_timer

# Default size
print(driver.get_window_size())

env = EncoderEvdev (valueChanged);
my_thread = threading.Thread(target=env.run)
my_thread.daemon = True
my_thread.start()

timer = 0

try:
    while True:
      url = readQRCode()
      if url in url_list:
          driver.get(url)
          currentPosition = 0
          max_scroll = driver.execute_script("return document.body.scrollHeight")
          #max_width = driver.execute_script("return document.body.scrollWidth")
          timer = reset_timer(timer)
except TimeoutError as e:
    print(e)
    driver.get("https://www.naver.com") #기본 페이지 display
    currentPosition = 0
    max_scroll = driver.execute_script("return document.body.scrollHeight")
except Exception:
    pass
