from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

def scrape_data(page_url):
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabulka")))

    speed_and_gust_lines = []
    category_group_lines = []
    direction_lines = []
    temp_lines = []

    # Extract wind speed
    speed_elements = driver.find_elements(By.CSS_SELECTOR, ".trow.param.WINDSPD")
    for element in speed_elements:
        try:
            first_line = element.text.split("\n")[0]
            speed_and_gust_lines.append(first_line)
        except Exception as e:
            print(f"Error extracting wind speed: {e}")

    # Extract gust
    gust_elements = driver.find_elements(By.CSS_SELECTOR, ".trow.param.GUST")
    for element in gust_elements:
        try:
            first_line = element.text.split("\n")[0]
            speed_and_gust_lines.append(first_line)
        except Exception as e:
            print(f"Error extracting gust: {e}")

    # Extract dates and hours
    category_groups = driver.find_elements(By.CLASS_NAME, "trow.tr_dates")
    for category_group in category_groups:
        try:
            text = category_group.text
            lines = text.split("\n")
            for i in range(0, len(lines) - 1, 2):
                if i + 1 < len(lines):
                    formatted_line = f"{lines[i]} {lines[i + 1]}"
                    category_group_lines.append(formatted_line)
        except Exception as e:
            print(f"Error extracting category group data: {e}")

    # Extract direction
    direction_elements = driver.find_elements(By.CSS_SELECTOR, ".trow.param.SMER")
    for direction_element in direction_elements:
        try:
            spans = direction_element.find_elements(By.TAG_NAME, "span")
            for span in spans:
                direction = span.get_attribute("title")
                if direction:
                    direction_lines.append(direction)
        except Exception as e:
            print(f"Error extracting direction data: {e}")

    # Extract temperature
    temp_elements = driver.find_elements(By.CLASS_NAME, "trow.param.TMPE")
    for category_group in category_groups:
        try:
            lines = category_group.text.split('\n')
            for line in lines:
                file.write(line + "\n")
        except Exception as e:
            print(f"Error: {e}")
    with open('temp.txt', 'r') as a:
        values = a.read().split()
    temp_lines = list(map(str, values))
    driver.quit()
    return speed_and_gust_lines, category_group_lines, direction_lines, temp_lines


# Function to extract first and fifth lines from a list and return them
def extract_first_and_fifth_lines(lines):
    lines_to_keep = []
    if len(lines) > 0:
        lines_to_keep.append(lines[0].strip())
    if len(lines) >= 5:
        lines_to_keep.append(lines[4].strip())
    return lines_to_keep

url = "https://www.windguru.cz/910318"

# Scrape data
speed_and_gust_lines, category_group_lines, direction_lines, temp_lines = scrape_data(url)

lines_to_keep = extract_first_and_fifth_lines(speed_and_gust_lines)

with open("wind_speed_gust.txt", "w", encoding="utf-8") as output_file:
    for line in lines_to_keep:
        output_file.write(line + "\n")

with open("dates.txt", "w", encoding="utf-8") as file:
    for line in category_group_lines[1:]:
        file.write(line + "\n")

with open("angles.txt", "w", encoding="utf-8") as file:
    for line in direction_lines:
        file.write(line + "\n")

with open("temp.txt", "w", encoding="utf-8") as file:
    for line in temp_lines:
        file.write(line + "\n")
