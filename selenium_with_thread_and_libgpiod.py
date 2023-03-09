from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from qr_read import readQRCode
from encoder_libgpiod import Encoder
import threading

url_list = ["https://www.naver.com/",
            "https://www.youtube.com/",
            "https://www.apple.com/"
            "https://github.com/"
            "https://google.com/"
            ]
handler_list = []

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
# Setup wait for later
wait = WebDriverWait(driver, 10)
handler_list.append(driver.current_window_handle)

for i, url in enumerate(site_list[1:]):
    # Opens a new tab and switches to new tab
    driver.switch_to.new_window('tab')
    driver.get(url)
    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(i+2))
    handler_list.append(driver.current_window_handle)

driver.switch_to.window(handler_list[site_list.index("https://www.naver.com/")])

env = Encoder(valueChanged);
my_thread = threading.Thread(target=env.run)
my_thread.daemon = True
my_thread.start()

timer = 0

try:
    while True:
      url = readQRCode()
      if url in url_list:
          #driver.get(url)
          driver.switch_to.window(handler_list[site_list.index(url)])
          timer = reset_timer(timer)
except Exception:
    pass

def valueChanged(value, direction):
    global driver
    global currentPosition
    global timer
    print("* New value: {}, Direction: {}".format(value, direction))
    if(direction == 'L'):
        driver.execute_script("window.scrollBy(0, 100)") 
    elif(direction == 'R'):
        driver.execute_script("window.scrollBy(0, -100)")     
    timer = reset_timer(timer)

def timeout():
    global timer
    if timer:
        timer.cancel()
    driver.switch_to.window(handler_list[site_list.index("https://www.naver.com/")]) #기본 페이지 display

def reset_timer(timer):
    if timer:
        timer.cancel()
    new_timer = threading.Timer(180, timeout)
    new_timer.daemon = True
    new_timer.start()
    return new_timer
