# Description: This script logs into LinkedIn and automatically likes all posts in the feed.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the chromedriver executable
chromedriver_path = r"X:\LinkedIn Automation\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.linkedin.com/login")
time.sleep(1)

USERNAME = "YOUR_EMAIL_ID" # Your LinkedIn username
PASSWORD = "PASSWORD" # Your LinkedIn password

wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2")))
time.sleep(1)

while True:
    time.sleep(1)
    like_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='React Like' and @aria-pressed='false']")
    if like_buttons:
        print(f"Found {len(like_buttons)} like button(s).")
        # Scroll each button into view and adjust the viewport
        for button in like_buttons:
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("window.scrollBy(0, -150);")
        time.sleep(1)
        # Click all like buttons concurrently via JavaScript
        driver.execute_script("arguments[0].forEach(btn => btn.click());", like_buttons)
        print("Clicked like buttons concurrently.")
        # Wait for UI change confirmation for each button
        for button in like_buttons:
            button_id = button.get_attribute("id")
            try:
                wait.until(EC.presence_of_element_located((
                    By.XPATH, f"//button[@id='{button_id}']//span[contains(@class, 'react-button__text--like')]"
                )))
                print(f"UI change confirmed for button with id: {button_id}")
            except Exception as e:
                print(f"Error confirming UI change for button id {button_id}: {e}")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolled down for new content...")
        time.sleep(1)
    else:
        try:
            show_more_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Show more feed updates')]]")
            driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
            driver.execute_script("window.scrollBy(0, -150);")
            time.sleep(1)
            show_more_y = show_more_button.location['y']
            driver.execute_script("arguments[0].click();", show_more_button)
            print("Clicked 'Show more feed updates' button.")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, arguments[0]);", show_more_y - 100)
            time.sleep(1)
        except Exception as e:
            print("No like or show more buttons found. Waiting...", e)
            time.sleep(1)
