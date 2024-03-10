# -------- Selenium ---------------
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create a webdriver instance (assuming Chrome)
# Create Chrome WebDriver instance with options
options = webdriver.ChromeOptions()
options.headless = False  # Set headless mode to False
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# Open the webpage with the Chart.js chart
driver.get('https://www.blockchaincenter.net/en/bitcoin-rainbow-chart/')

time.sleep(10)
# Find the canvas element representing the chart
chart_canvas = driver.find_element_by_id('rainbow')

# Get the x and y coordinates of the canvas
x_coord = chart_canvas.location['x']
y_coord = chart_canvas.location['y']

# Create an ActionChains object and move to the canvas element
action = ActionChains(driver)
action.move_to_element(chart_canvas)  # Adjust offset as needed
action.perform()

# Wait for the tooltip to appear
tooltip = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.chartjs-tooltip')))

# Extract the tooltip content
tooltip_content = tooltip.text
print(tooltip_content)
# Close the webdriver
driver.quit()