from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random as rand

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1080, 800)  # Set the size of the window

# Navigate to your Depop shop
url = "https://www.depop.com/SHOP_NAME/" 
driver.get(url)

time.sleep(rand.uniform(2, 3))

# Bypass cookie banner to interact with website
try:
    # Locate the "Accept" button using its data-testid attribute
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='cookieBanner__acceptAllButton']"))
    )
    cookie_button.click()  # Click the accept button
    print("Cookie banner accepted.")

except Exception as e:
    print("No cookie banner found or unable to click the button:", e)

time.sleep(rand.uniform(2, 3))

# Scroll to bottom of page to load all items before scraping
while True:

    item_containers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_listItem__uQkGy'))
    )

    last_item = item_containers[-1]
    
    try:
        sold_overlay = last_item.find_element(By.CLASS_NAME, 'styles_gradientOverlay__eIVYO')
        print("Reached bottom of available items.")

    except Exception as e:
        sold_overlay = False
    
    if sold_overlay:
        break
    

    # Scroll down by a small amount to load more items
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll down in increments
    time.sleep(rand.uniform(4, 6))  # Wait for items to load

item_data = []
# Wait for item containers to load
item_containers = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_listItem__uQkGy'))
)
# Extract data from the current batch of items
for item in item_containers:
    try: 
        sold_overlay = item.find_element(By.CLASS_NAME, 'styles_gradientOverlay__eIVYO')
        print("Scraped all listed items.")
        break

    except:
        try:
            # Extract the item link
            link_element = item.find_element(By.CSS_SELECTOR, 'a[data-testid="extendedLinkAnchor"]')
            link = link_element.get_attribute('href')

            # Extract image link
            image_link_element = item.find_element(By.CLASS_NAME, '_mainImage_e5j9l_11')
            image_link = image_link_element.get_attribute('src')

            # Extract the price
            price_element = item.find_element(By.CLASS_NAME, 'styles_price__H8qdh')
            price = price_element.text.strip()
            # Append to data list
            item_data.append({'Item URL': link, 'Image URL': image_link, 'Price': price})
        except Exception as e:
            print(f"Error extracting item data: {e}")

# Save the data to a CSV file
df = pd.DataFrame(item_data)
df.to_csv(r'\Your\Path\Here', index=False)

# Close the driver
driver.quit()
