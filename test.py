from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of a Chrome driver
driver = webdriver.Chrome()

# Function to scrape data from a single page and write to file
def scrape_data(page_url, file):
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabulka")))

    # Find all elements with the specified class name
    category_groups = driver.find_elements(By.CLASS_NAME, "trow.param.TMPE")

    for category_group in category_groups:
        try:
            lines = category_group.text.split('\n')
            for line in lines:
                file.write(line + "\n")  # Write each line separately to file
        except Exception as e:
            print(f"Error: {e}")

# Open file to append data
# Read the content from the file
with open("temp.txt", "r") as file:
    content = file.read()

# Split the content by spaces
numbers = content.split()

# Write each number to a new line in the file
with open("temp.txt", "w") as file:
    for number in numbers:
        file.write(number + "\n")

# Close the browser
driver.quit()
