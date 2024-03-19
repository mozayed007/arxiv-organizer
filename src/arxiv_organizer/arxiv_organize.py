import os
import shutil
from pathlib import Path
import arxiv
import json
import logging
import re
import importlib
logging.basicConfig(level=logging.INFO)

def extract_paper_id(title):
    """Return the paper ID from the title."""
    return title.split('_')[2].split('.pdf')[0]

def fetch_paper_metadata(paper_id):
    """Fetch and return the metadata for the paper with the given ID."""
    logging.info(f"Fetching metadata for paper {paper_id}")
    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results())
    if paper:
        logging.info(f"Metadata for paper {paper_id} fetched successfully")
        return paper
    logging.warning(f"No metadata found for paper {paper_id}")
    return None

def move_papers_to_subcategories(folder_path):
    """Move papers in the given folder to subcategories based on their metadata."""
    logging.info(f"Moving papers in folder {folder_path} to subcategories")

    # Check if the folder is named 'arxiv'
    if os.path.basename(folder_path) != 'arxiv':
        logging.error(f"Error: The folder {folder_path} is not named 'arxiv'")
        return

    # Load the category mapping
    try:
        categories_file = importlib.resources.files('arxiv_organizer').joinpath('utils', 'categories.json')
        with open(categories_file, 'r') as f:
            category_mapping = json.load(f)
    except FileNotFoundError:
        logging.error("Error: categories.json file not found")
        return

    for paper in os.listdir(folder_path):
        if not paper.endswith('.pdf'):  # Skip non-PDF files
            continue

        if not re.match(r"[\w']+_\w+_\d{4}\.\d{4,5}(v\d+)?\.pdf", paper):
            logging.warning(f"Skipping file {paper} because its name does not match the expected format")
            continue
        logging.info(f"Processing paper {paper}")
        paper_id = extract_paper_id(paper)
        logging.info(f"Extracted paper ID: {paper_id}")
        paper_metadata = fetch_paper_metadata(paper_id)
        if paper_metadata:
            category = paper_metadata.primary_category
            logging.info(f"Category for paper {paper_id}: {category}")

            # Map the category to the folder name
            if '.' in category:
                main_category, sub_category = category.split('.')
            else:
                main_category = category
                sub_category = None

            # Use only the main category when the subcategory is empty
            if sub_category:
                folder_name = category_mapping.get(main_category, {}).get(category, 'Unknown')
            else:
                folder_name = category_mapping.get(main_category, {}).get(main_category, 'Unknown')
            subcategory_folder = Path(folder_path) / main_category / folder_name
            logging.info(f"Subcategory folder path: {subcategory_folder}")

            subcategory_folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created subcategory folder: {subcategory_folder}")

            # Check if the paper already exists in the destination folder
            if (subcategory_folder / paper).exists():
                logging.info(f"Paper {paper_id} already exists in {subcategory_folder}, skipping")
                continue

            shutil.move(os.path.join(folder_path, paper), os.path.join(subcategory_folder, paper))
            logging.info(f"Moved paper {paper_id} to {subcategory_folder}")
        else:
            logging.warning(f"No metadata for paper {paper}, skipping")
    logging.info(f"Finished moving papers in folder {folder_path} to subcategories")