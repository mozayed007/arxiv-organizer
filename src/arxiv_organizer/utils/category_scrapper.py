from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import traceback
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def update_categories():
    """Scrape the latest categories and update the categories.json file."""
    logger.info("Updating categories")
    categories = scrape_categories()
    categories_file = Path(__file__).parent / 'categories.json'

    try:
        with open(categories_file, 'w') as f:
            json.dump(categories, f, indent=4)
        logger.info(f"Categories saved to {categories_file}")
    except Exception as e:
        logger.error(f"Error saving categories to JSON file: {e}")


def scrape_categories() -> dict:
    """Scrape categories from arXiv and return them as a dictionary."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get('https://arxiv.org/category_taxonomy')

        expand_elements = driver.find_elements(By.CSS_SELECTOR, 'h2.accordion-head')
        main_categories = {element.get_attribute('id'): element.text for element in expand_elements}

        category_elements = driver.find_elements(By.CSS_SELECTOR, 'div.accordion-body div.columns div.column.is-one-fifth > h4')
        categories = {}

        for element in category_elements:
            try:
                text = element.text
                if text:
                    parts = text.split(' ')
                    if len(parts) > 1:
                        abbreviation = parts[0]
                        full_name = element.find_element(By.TAG_NAME, 'span').text.strip('()')
                        main_category_abbr = abbreviation.split('.')[0]
                        main_category_name = main_categories.get(main_category_abbr, main_category_abbr)

                        if main_category_abbr not in categories:
                            categories[main_category_abbr] = {}
                        categories[main_category_abbr][abbreviation] = full_name
            except Exception as e:
                logger.error(f"Error processing element {element.text}:")
                traceback.print_exc()
    finally:
        driver.quit()
    return categories
