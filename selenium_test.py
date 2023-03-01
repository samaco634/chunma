from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time


option = Options()
option.add_argument("--start-maximized")
option.add_argument("--no-sandbox")
option.add_argument("--disable-web-security")
option.add_argument("--ignore-certificate-errors")
#option.add_argument("--kiosk")
option.add_argument("--disable-password-manager-reauthentication")
option.add_argument("--disable-infobars")
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=option)
driver.get("http://naver.com")

driver.execute_script("""var myhistory = []

document.addEventListener("keydown", keyDownTextField, false);

function keyDownTextField(e) {
var keyCode = e.keyCode;
  myhistory.push(keyCode)
}""")
def get_history():
    return browser.execute_script("myhistory")

# now wait for a while and type on the browser
import time; time.sleep(5000)

print("keys:", get_history())

