from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Set up Selenium WebDriver for Brave
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: Runs Brave in headless mode
chrome_options.binary_location = "/usr/bin/google-chrome"  # Path to Brave executable

# Path to ChromeDriver
service = Service('/usr/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Cricbuzz match commentary page
url = "https://www.espncricinfo.com/series/india-in-sri-lanka-2024-1442984/sri-lanka-vs-india-3rd-odi-1442992/ball-by-ball-commentary"  # Replace XXXXX with match ID

# Open the URL
driver.get(url)

# Extract commentary elements
commentary_elements = driver.find_elements(By.CSS_SELECTOR, 'div.first-letter:ds-capitalize')

# Extract text from elements
commentary_text = [element.text for element in commentary_elements]

# Optionally, save to CSV
df = pd.DataFrame(commentary_text, columns=["Commentary"])
df.to_csv("match_commentary.csv", index=False)

print("Commentary saved to match_commentary.csv")

# Close the WebDriver
driver.quit()
