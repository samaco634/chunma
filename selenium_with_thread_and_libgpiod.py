from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 

import sys

import time
from qr_read import readQRCode
from encoder_libgpiod import Encoder
#from encoder_libgpiod2 import Encoder #offset 값 확인 할 것
import threading

url_list = ["https://www.naver.com/",
            "https://www.youtube.com/",
            "https://www.apple.com/",
            "https://github.com/",
            "https://www.waterpik.co.kr/product/index.asp?svc_name=product&lst_cate1=P0001&lst_cate2=P0012&ptype=view&p_code=P0028"
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

driver = webdriver.Chrome(service=Service('/usr/lib/chromium-browser/chromedriver'), options = option)
driver.get("https://www.naver.com")
# Setup wait for later
wait = WebDriverWait(driver, 10)
handler_list.append(driver.current_window_handle)

for i, url in enumerate(url_list[1:]):
    # Opens a new tab and switches to new tab
    driver.switch_to.new_window('tab')
    driver.get(url)
    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(i+2))
    handler_list.append(driver.current_window_handle)

driver.switch_to.window(handler_list[url_list.index("https://www.naver.com/")])

def valueChanged(value, direction):
    global driver
    global timer
    scroll_val = 0
    print("* New value: {}, Direction: {}".format(value, direction))
    if(direction == 'L'):
        #currentPosition -= 100
        #if(currentPosition < 0):
        #    currentPosition = 0
        scroll_val = -100
    elif(direction == 'R'):
        #currentPosition += 100
        #if(currentPosition > max_scroll):
        #    currentPosition = max_scroll
        scroll_val = 100
    #print("current position {}, last_height {}".format(currentPosition, max_scroll))
    #driver.execute_script("window.scrollTo(0, "+str(currentPosition)+")") 
    driver.execute_script("window.scrollBy(0, "+str(scroll_val)+")")
    timer = reset_timer(timer)

def timeout():
	global timer
	global driver
	driver.switch_to.window(handler_list[url_list.index("https://www.naver.com/")]) #기본 페이지 display
	scroll_to_top()
	timer.cancel()

def reset_timer(timer):
    if timer:
        timer.cancel()
    new_timer = threading.Timer(180, timeout)
    new_timer.daemon = True
    new_timer.start()
    return new_timer

def scroll_to_top():
	global driver
	#htmlelement=driver.find_element(By.TAG_NAME, "html")
	#Scrolls up to the top of the page
	#htmlelement.send_keys(Keys.HOME)
	driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)	

# Default size
print(driver.get_window_size())

env = Encoder(valueChanged);
my_thread = threading.Thread(target=env.run)
my_thread.daemon = True
my_thread.start()

timer = 0

try:
	while True:
		url = readQRCode()
		if url in url_list:
			driver.switch_to.window(handler_list[url_list.index(url)])
			scroll_to_top()
			timer = reset_timer(timer)
except Exception as e: # work on python 3.x
    print(str(e))
    pass
