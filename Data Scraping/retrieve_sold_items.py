from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random as rand

# Login credentials
username = 'username'
password = 'password'

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1080, 800)  # Set the size of the window

# Navigate to Depop login page
login_url = 'https://www.depop.com/login/'
driver.get(login_url)

time.sleep(rand.uniform(2, 3)) # Pause to appease Depop servers

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

# Find the username and password fields and the login button
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'username__input'))
)

time.sleep(rand.uniform(2, 5)) # Pause to appease Depop servers

# Enter your credentials
username_input = driver.find_element(By.ID, 'username__input')
username_input.send_keys(username)

time.sleep(rand.uniform(2, 5)) # Pause to appease Depop servers

password_input = driver.find_element(By.ID, 'password__input')
password_input.send_keys(password)

# Click the login button
login_button = driver.find_element(By.XPATH, "//button[@data-testid='login__cta']")  # Use the data-testid to locate the button

time.sleep(rand.uniform(2, 5)) # Pause to appease Depop servers

login_button.click()

# Prompt for 2FA code
two_fa_code = input("Please enter your 2FA code: ")  # Wait for user input

time.sleep(rand.uniform(20, 30)) # Pause to allow you to enter code

# Find the 2FA input field and enter the code
try:
    # Loop through the six inputs and enter each digit of the 2FA code
    for i in range(6):
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@data-testid='verification-code__input-{i}']"))
        )
        input_field.send_keys(two_fa_code[i])  # Enter the corresponding digit
    
    # Optionally click the submit button for the 2FA
    submit_button = driver.find_element(By.XPATH, "//button[@data-testid='mfa__otp-submit']")
    submit_button.click()

except Exception as e:
    print("Error while entering 2FA code:", e)

time.sleep(rand.uniform(2, 5)) # Pause to appease Depop servers

# Directly navigate to the hub URL in the same tab
hub_url = "https://www.depop.com/sellinghub/sold-items/"
driver.get(hub_url)  # Change to direct navigation

# Scroll to bottom of page to load all items before scraping
previous_scroll_position = driver.execute_script("return window.pageYOffset;")

while True:
    # Scroll down by a small amount to load more items
    driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down in increments
    time.sleep(rand.uniform(4, 7))  # Wait for items to load

    # Get the current scroll position
    current_scroll_position = driver.execute_script("return window.pageYOffset;")
    
    # Check if we've reached the bottom (no change in scroll position)
    if current_scroll_position <= previous_scroll_position:
        print("Reached the bottom of the list.")
        break

    previous_scroll_position = current_scroll_position

# Data scraping logic (similar to previous examples)
item_data = []
driver.execute_script("window.scrollTo(0, 0);")

# Set max number of items to extract data from
item_count = 0
max_item_count = 451

while True:

    if item_count >= max_item_count:
        break
    
    # Wait for item containers to load
    item_containers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ReceiptsList-styles__ReceiptListWrapper-sc-55d3004f-1"))
    )
    # Extract data from the current batch of items
    for item in item_containers:

        item_count += 1

        try:
            date_element = item.find_element(By.XPATH, ".//div[@data-testid='receipt__sold_on']")
            date = date_element.find_elements(By.TAG_NAME, 'span')[-1].text.strip()
            location = item.find_elements(By.CLASS_NAME, "index-styles__LocationDetails-sc-971ea662-3")[-1].text
            item_image = item.find_element(By.CLASS_NAME, "ImageStack-styles__Container-sc-81f7be5e-0")
            item_image.click()
            time.sleep(rand.uniform(2, 5))
            item_receipts = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "styles__ProductLink-sc-233ee08-7"))
            )
            for item_receipt in item_receipts:
                try:
                    # Extract item image
                    img_link = item_receipt.find_element(By.TAG_NAME, 'img').get_attribute('src')

                    # Extract secondary information
                    info_tag = item_receipt.find_element(By.CLASS_NAME, "styles__ProductInformation-sc-233ee08-2").find_elements(By.TAG_NAME, 'p')

                    # info_tag varies based on item type and whether its discounted
                    if len(info_tag) < 4:
                        description = info_tag[0].text
                        size = 'One Size'
                        price_listed = info_tag[1].text
                        price_sold = info_tag[1].text
                        brand = info_tag[2].text
                    elif len(info_tag) == 4:
                        description = info_tag[0].text
                        size = info_tag[1].text
                        price_listed = info_tag[2].text
                        price_sold = info_tag[2].text
                        brand = info_tag[3].text
                    else:
                        description = info_tag[0].text
                        size = info_tag[1].text
                        price_listed = info_tag[2].text
                        price_sold = info_tag[3].text
                        brand = info_tag[4].text

                    # Collect data
                    item_data.append({
                        'Image': img_link,
                        'Description': description,
                        'Price listed': price_listed,
                        'Price sold': price_sold,
                        'Size': size,
                        'Brand': brand,
                        'Date': date,
                        'Location': location
                    })
                    time.sleep(rand.uniform(2, 5)) # Pause to appease Depop servers

                except Exception as e:
                    print(f"Error extracting receipt data: {e}")

            if item_count >= max_item_count:
                break

        except Exception as e:
            print(f"Error extracting item data: {e}")

# Define the path to save the CSV file on the desktop
desktop_path = r'Your\Path\Here'  # Use your desktop path

# Save the data to a CSV file
df = pd.DataFrame(item_data)
print(df)
df.to_csv(desktop_path, index=False)

# Close the driver
driver.quit()
