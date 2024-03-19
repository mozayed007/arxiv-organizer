from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import traceback
import logging
from pathlib import Path


def update_categories():
    """Scrape the latest categories and update the categories.json file."""
    logging.info("Updating categories")

    # Scrape the categories (replace this with your actual scraping code)
    categories = scrape_categories()

    # Get the path to the categories.json file
    categories_file = Path(__file__).parent / 'categories.json'

    # Log the content of categories
    logging.info(f"Scraped categories: {categories}")
    # Save the categories to a JSON file
    try:
        with open(categories_file, 'w') as f:
            json.dump(categories, f, indent=4)
        print("Categories saved to categories.json")
    except Exception as e:
        print("Error saving categories to JSON file:")
        traceback.print_exc()
    logging.info(f"Updated categories in {categories_file}")
def scrape_categories():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Navigate to the arXiv taxonomy page
    driver.get('https://arxiv.org/category_taxonomy')

    # Find the elements that expand the category sections
    expand_elements = driver.find_elements(By.CSS_SELECTOR, 'h2.accordion-head')

    # Initialize an empty dictionary to store the main categories
    main_categories = {}

    # Click each element to expand the section and extract main categories
    for element in expand_elements:
        element.click()
        main_category_name = element.text
        main_category_abbr = element.get_attribute('id')
        main_categories[main_category_abbr] = main_category_name

    # Find the elements that contain the category information
    try:
        category_elements = driver.find_elements(By.CSS_SELECTOR, 'div.accordion-body div.columns div.column.is-one-fifth > h4')
        print(f"Found {len(category_elements)} category elements")
    except Exception as e:
        print("Error finding category elements:")
        traceback.print_exc()

    # Initialize an empty dictionary to store the categories
    categories = {}

    # Iterate over the category elements
    for element in category_elements:
        try:
            # Extract the category abbreviation and full name
            text = element.text
            if text:
                parts = text.split(' ')
                if len(parts) > 1:
                    abbreviation = parts[0]
                    full_name = element.find_element(By.TAG_NAME, 'span').text.strip('()')

                    # Debug print
                    print(f"Extracted category: {abbreviation} - {full_name}")

                    # Extract the main category
                    main_category_abbr = abbreviation.split('.')[0]
                    main_category_name = main_categories.get(main_category_abbr, main_category_abbr)

                    # Add the category to the dictionary
                    if main_category_name not in categories:
                        categories[main_category_name] = {}
                    categories[main_category_name][abbreviation] = full_name
                else:
                    print(f"Unexpected format for element text: {text}")
            else:
                print("Element text is empty")
        except Exception as e:
            print(f"Error processing element {element.text}:")
            traceback.print_exc()

    # Close the WebDriver
    driver.quit()
    # Return the categories instead of writing them to the file
    return categories
