"""
Amazon Deals Scraper - Beginner Friendly Version
=================================================
This script crawls Amazon deals and saves them to a CSV file.

What you need to install:
    pip install selenium webdriver-manager

How to run:
    python crawl.py
"""

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ===== SETTINGS =====
START_URL = "https://www.amazon.sg/s?k=amazon+deals"
OUTPUT_CSV = "deals.csv"
MAX_PAGES = None  # None means scrape all pages, or set a number like 5
WAIT_TIME = 2  # seconds to wait between pages


# ===== STEP 1: Setup Chrome Browser =====
def create_driver():
    """Creates and returns a Chrome browser that runs in the background."""
    # Setup browser options
    options = Options()
    options.add_argument("--headless=new")  # Run without opening a window
    options.add_argument("--no-sandbox") # Disable the security sandbox (may be needed in some environments)
    options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems (64MB by default for RAM usage)

    # Create and return the browser
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ===== STEP 2: Scrape Products from Current Page =====
def scrape_page(driver):
    """Gets all product deals from the current page."""

    # Wait for products to load (up to 10 seconds)
    # until the element with attribute data-component-type="s-search-result" is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
        )
    )
    product_cards = driver.find_elements(
        By.CSS_SELECTOR, '[data-component-type="s-search-result"]'
    )

    # Extract data from each product card
    all_deals = []
    for card in product_cards:
        deal = extract_deal(card)
        if deal:  # Only add if we got valid data
            all_deals.append(deal)

    return all_deals


# ===== STEP 3: Extract Data from One Product Card =====
def extract_deal(card):
    """Gets brand, product name, prices, and image from a product card."""

    try:
        # Get all title spans (brand is first, product name is second)
        title_spans = card.find_elements(By.CSS_SELECTOR, "h2 span")

        # Get brand name from first span
        if len(title_spans) > 0:
            brand_name = title_spans[0].text.strip()
        else:
            brand_name = None

        # Get product name from second span
        if len(title_spans) > 1:
            product_name = title_spans[1].text.strip()
        else:
            product_name = None

        # Skip if no brand or product name found
        if not brand_name and not product_name:
            return None

        # Get current price (price after discount)
        price_elements = card.find_elements(By.CSS_SELECTOR, ".a-price .a-offscreen")
        if price_elements:
            price_after = price_elements[0].get_attribute("textContent").strip()
        else:
            price_after = None

        # Get original price (price before discount)
        original_price_elements = card.find_elements(By.CSS_SELECTOR, ".a-text-price .a-offscreen")
        if original_price_elements:
            price_before = original_price_elements[0].get_attribute("textContent").strip()
        else:
            price_before = None

        # Get product image URL
        image_elements = card.find_elements(By.CSS_SELECTOR, "img.s-image")
        if image_elements:
            image_url = image_elements[0].get_attribute("src")
        else:
            image_url = None

        # Return the product data as a dictionary
        return {
            "brand_name": brand_name,
            "product_name": product_name,
            "price_before": price_before,
            "price_after": price_after,
            "image_url": image_url,
        }

    except Exception:
        # If anything goes wrong, skip this product
        return None


# ===== STEP 4: Go to Next Page =====
def go_to_next_page(driver):
    """Clicks the 'Next' button. Returns True if successful, False if no more pages."""

    try:
        # Find the Next button
        next_button = driver.find_element(By.CSS_SELECTOR, ".s-pagination-next")

        # Check if button is disabled (last page)
        button_classes = next_button.get_attribute("class") or ""
        if "s-pagination-disabled" in button_classes:
            return False  # No more pages

        # Click the button and wait
        next_button.click()
        time.sleep(WAIT_TIME)
        return True

    except Exception:
        # Button not found, so we're on the last page
        return False


# ===== STEP 5: Save All Deals to CSV File =====
def save_to_csv(deals, filename):
    """Saves the list of deals to a CSV file."""

    if not deals:
        print("No deals to save.")
        return

    # Open file and write data
    with open(filename, "w", newline="", encoding="utf-8") as file:
        # Get column names from first deal
        columns = deals[0].keys()
        writer = csv.DictWriter(file, fieldnames=columns)

        # Write header row
        writer.writeheader()

        # Write all deals
        writer.writerows(deals)

    print(f"\nSaved {len(deals)} deals to {filename}")


# ===== STEP 6: Main Program - Put It All Together =====
def main():
    """Main function that runs the entire scraper."""

    # Start the browser
    print("Starting browser...")
    driver = create_driver()

    # This will store all deals from all pages
    all_deals = []

    try:
        # Open the Amazon deals page
        print(f"Opening {START_URL}")
        driver.get(START_URL)
        time.sleep(WAIT_TIME)

        # Loop through pages
        page_number = 1
        while True:
            print(f"Scraping page {page_number}...", end=" ")

            # Get all deals from current page
            deals_on_page = scrape_page(driver)
            all_deals.extend(deals_on_page)

            print(f"Found {len(deals_on_page)} deals (Total so far: {len(all_deals)})")

            # Check if we should stop
            if MAX_PAGES and page_number >= MAX_PAGES:
                print(f"Reached the page limit of {MAX_PAGES} pages.")
                break

            # Try to go to next page
            if not go_to_next_page(driver):
                print("No more pages available.")
                break

            page_number += 1

    finally:
        # Always close the browser when done
        print("Closing browser...")
        driver.quit()

    # Save all deals to CSV file
    save_to_csv(all_deals, OUTPUT_CSV)


# Run the program
if __name__ == "__main__":
    main()