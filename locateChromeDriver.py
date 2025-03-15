# If you are unable to find where chromedriver was installed, use this script
from selenium import webdriver

driver = webdriver.Chrome()
ChromeDriverLocation = driver.service.path
print(ChromeDriverLocation)
