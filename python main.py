import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# =========================================================
# CONFIGURATION
# =========================================================

WHATSAPP_URL = "https://web.whatsapp.com/"

CHROMIUM_PATH = "/data/data/com.termux/files/usr/bin/chromium-browser"
CHROMEDRIVER_PATH = "/data/data/com.termux/files/usr/bin/chromedriver"


# =========================================================
# DRIVER SETUP
# =========================================================

def create_driver():
    options = webdriver.ChromeOptions()

    # Termux Chromium
    options.binary_location = CHROMIUM_PATH

    # Android/Termux options
    # QR code dekhne ke liye headless OFF rakha hai.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")

    service = Service(CHROMEDRIVER_PATH)

    return webdriver.Chrome(
        service=service,
        options=options
    )


# =========================================================
# MAIN
# =========================================================

def open_whatsapp():
    print("DIG: Initializing Chromium...")

    driver = None

    try:
        driver = create_driver()

        print("DIG: Chromium started successfully.")

        driver.get(WHATSAPP_URL)

        print(f"DIG: Navigating to {WHATSAPP_URL}")
        print()
        print("--- AUTHENTICATION MODE ---")
        print("DIG: Scan the WhatsApp Web QR code.")

        try:
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"]')
                )
            )

            print("DIG: WhatsApp Web authentication detected.")

        except TimeoutException:
            print("DIG ERROR: QR authentication timed out.")
            return

        print("DIG: WhatsApp Web is ready.")

        # Keep browser open
        while True:
            time.sleep(1)

    except Exception as e:
        print()
        print("!!! FATAL DIG ERROR !!!")
        print(e)

    finally:
        if driver is not None:
            print("DIG: Closing browser.")
            driver.quit()


if __name__ == "__main__":
    open_whatsapp()
