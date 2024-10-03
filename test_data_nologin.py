from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1080, 800)  # Set the size of the window

# Navigate to your Depop shop
url = "https://www.depop.com/madvirgies/"
driver.get(url)

item_data = []
# Wait for item containers to load
item_containers = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_listItem__uQkGy'))
)
# Extract data from the current batch of items
for item in item_containers:
    try:
        # Extract the item link
        link_element = item.find_element(By.CSS_SELECTOR, 'a[data-testid="extendedLinkAnchor"]')
        link = link_element.get_attribute('href')
        
        # Extract the price
        price_element = item.find_element(By.CLASS_NAME, 'styles_price__H8qdh')
        price = price_element.text.strip()
        # Append to data list
        item_data.append({'URL': link, 'Price': price})
    except Exception as e:
        print(f"Error extracting item data: {e}")

# Save the data to a CSV file
df = pd.DataFrame(item_data)
df.to_csv(r'c:\Users\legat\OneDrive\Desktop\depop_items_scraped.csv', index=False)

# Close the driver
driver.quit()
