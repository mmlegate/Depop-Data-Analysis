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
driver.set_window_size(1080, 1080)  # Set the size of the window

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
    driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down in increments
    time.sleep(rand.uniform(6, 8))  # Wait for items to load

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

time.sleep(rand.uniform(4, 6))

# Save the data to a CSV file
df = pd.DataFrame(item_data)
df = df.iloc[2:] # First two posts are promotional, not products. Adjust as needed

other_data = []

for item_url in df['Item URL']:

    driver.get(item_url)
    wrapper = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'styles__ContentWrapper-sc-b6f63023-5'))
    )
    time.sleep(rand.uniform(4, 7))
    try: 
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'styles__ShowMoreButton-sc-d367c36f-4'))
        )
        show_more_button.click()

    except:
        print("No 'Show More' button found or unable to click.")

    try:
        info_element = wrapper.find_elements(By.CLASS_NAME, 'ProductAttributes-styles__Attribute-sc-303d66c3-0')
        if len(info_element) < 6 and len(info_element[3].text) > 9:
            size = 'One Size'
            brand = info_element[-1].text
        elif len(info_element) < 6:
            size = info_element[3].text
            brand = 'Other'
        else:
            size = info_element[3].text
            brand = info_element[-1].text

        description = wrapper.find_element(By.XPATH, ".//div[@data-testid='product__description']").text
        other_data.append({'Size': size, 'Brand': brand, 'Description': description})
        time.sleep(rand.uniform(2, 5))

    except Exception as e:
        print(f"Error extracting item data from {item_url}: {e}")
        break

other_df = pd.DataFrame(other_data)
df = df.drop(columns=['Item URL'])
df = pd.concat([df.reset_index(drop=True), other_df.reset_index(drop=True)], axis=1)

df.to_csv(r'C:\Your\Path\Here', index=False)
print("Dataframe saved!")

# Close the driver
driver.quit()
