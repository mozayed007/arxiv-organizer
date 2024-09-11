from pathlib import Path
import argparse
from . import move_papers, move_papers_to_subcategories, update_categories
import time
import importlib.resources
from .arxiv_organize import setup_logging

def process_papers():
    setup_logging()
    parser = argparse.ArgumentParser(description='Organize arXiv papers.')
    parser.add_argument('--update-categories', action='store_true', help='Update the categories')
    parser.add_argument('--directory', type=str, help='The directory to process')
    args = parser.parse_args()

    directory = Path(args.directory) if args.directory else Path.cwd()

    categories_file = importlib.resources.files('arxiv_organizer').joinpath('utils', 'categories.json')
    if not categories_file.exists():
        print(f"Error: {categories_file} does not exist.")
        return

    if args.update_categories or is_categories_file_old(categories_file):
        update_categories()

    move_papers(directory)
    move_papers_to_subcategories(directory / 'arxiv')

def is_categories_file_old(categories_file: Path) -> bool:
    """Check if categories.json was modified more than 3 months ago."""
    modification_time = categories_file.stat().st_mtime
    return time.time() - modification_time > 3 * 30 * 24 * 60 * 60  # 3 months in seconds

if __name__ == "__main__":
    process_papers()