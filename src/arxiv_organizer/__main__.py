from pathlib import Path
import argparse
from . import move_papers, move_papers_to_subcategories, update_categories
import time
import os
import importlib.resources

def process_papers():
    parser = argparse.ArgumentParser(description='Organize arXiv papers.')
    parser.add_argument('--update-categories', action='store_true', help='Update the categories')
    parser.add_argument('--directory', type=str, help='The directory to process')
    args = parser.parse_args()

    # Use the current directory if no directory was provided
    directory = args.directory if args.directory else os.getcwd()

    # Check if categories.json exists
    categories_file = importlib.resources.files('arxiv_organizer').joinpath('utils', 'categories.json')
    if not categories_file.exists():
        print(f"Error: {categories_file} does not exist.")
        return
    elif args.update_categories:
        update_categories()
    else:
        # Check if categories.json was modified more than 3 months ago
        modification_time = categories_file.stat().st_mtime
        if time.time() - modification_time > 3 * 30 * 24 * 60 * 60:  # 3 months in seconds
            update_categories()

    move_papers(directory)
    move_papers_to_subcategories(directory+'/arxiv')

if __name__ == "__main__":
    process_papers()