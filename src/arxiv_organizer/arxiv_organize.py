import os
import shutil
from pathlib import Path
import arxiv
import json
import logging
import re
import importlib.resources

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def extract_paper_id(title: str) -> str:
    """Return the paper ID from the title."""
    return title.split('_')[2].split('.pdf')[0]

def fetch_paper_metadata(paper_id: str) -> arxiv.Result:
    """Fetch and return the metadata for the paper with the given ID."""
    logging.info(f"Fetching metadata for paper {paper_id}")
    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results(), None)
    if paper:
        logging.info(f"Metadata for paper {paper_id} fetched successfully")
        return paper
    logging.warning(f"No metadata found for paper {paper_id}")
    return None

def move_papers_to_subcategories(folder_path: Path):
    """Move papers in the given folder to subcategories based on their metadata."""
    logging.info(f"Moving papers in folder {folder_path} to subcategories")

    if folder_path.name != 'arxiv':
        logging.error(f"Error: The folder {folder_path} is not named 'arxiv'")
        return

    try:
        categories_file = importlib.resources.files('arxiv_organizer').joinpath('utils', 'categories.json')
        with open(categories_file, 'r') as f:
            category_mapping = json.load(f)
    except FileNotFoundError:
        logging.error("Error: categories.json file not found")
        return

    for paper in folder_path.glob('*.pdf'):
        if not re.match(r"[\w']+_\w+_\d{4}\.\d{4,5}(v\d+)?\.pdf", paper.name):
            logging.warning(f"Skipping file {paper.name} because its name does not match the expected format")
            continue

        logging.info(f"Processing paper {paper.name}")
        paper_id = extract_paper_id(paper.name)
        paper_metadata = fetch_paper_metadata(paper_id)
        if paper_metadata:
            category = paper_metadata.primary_category
            logging.info(f"Category for paper {paper_id}: {category}")

            main_category, sub_category = category.split('.') if '.' in category else (category, None)
            folder_name = category_mapping.get(main_category, {}).get(category, 'Unknown')
            subcategory_folder = folder_path / main_category / folder_name

            subcategory_folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created subcategory folder: {subcategory_folder}")

            if (subcategory_folder / paper.name).exists():
                logging.info(f"Paper {paper_id} already exists in {subcategory_folder}, skipping")
                continue

            shutil.move(str(paper), str(subcategory_folder / paper.name))
            logging.info(f"Moved paper {paper_id} to {subcategory_folder}")
        else:
            logging.warning(f"No metadata for paper {paper.name}, skipping")
    logging.info(f"Finished moving papers in folder {folder_path} to subcategories")