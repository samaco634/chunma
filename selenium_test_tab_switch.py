from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import KEYS
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Listener

import time


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

site_list = [ "https://naver.com",
                "https://youtube.com",
                "https://google.com",
                "https://github.com/"
            ]
                
handler_list = []

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=option)
driver.get("https://naver.com")
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

driver.switch_to.window(handler_list[site_list.index("https://youtube.com")])

def on_press(key):
    if key == Key.right:
        driver.execute_script("window.scrollBy(0, 100)") 
    elif key == Key.left:
        driver.execute_script("window.scrollBy(0, -100)") 

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
