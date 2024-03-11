# -------- Selenium ---------------
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from seleniumbase import Driver


# Create a webdriver instance (assuming Chrome)
# Create Chrome WebDriver instance with options

options = webdriver.ChromeOptions()
options.headless = False  # Set headless mode to False
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)


# Open the webpage with the Chart.js chart
driver.get('https://coinmarketcap.com/new/')
# Find all <html> elements
time.sleep(5)
html_elements = driver.find_elements(by=By.TAG_NAME, value='html')

# Extract text content from each <html> element
page_text = "\n".join(html_element.text for html_element in html_elements)

# Close the webdriver

# Print the text content
print(page_text)