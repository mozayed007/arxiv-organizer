import os
from pathlib import Path
import re    # regular expressions
import arxiv # python wrapper for arxiv api
import logging

logging.basicConfig(level=logging.INFO)

def get_files(current_dir):
    """Return a list of PDF files in the current directory whose names match the arXiv ID pattern."""
    all_pdfs = list(Path(current_dir).rglob("*.pdf"))
    arxiv_pdfs = [pdf for pdf in all_pdfs if re.match(r'\d{4}\.\d{5}(v\d+)?.pdf', pdf.name)]
    return arxiv_pdfs

def create_save_dir(current_dir):
    """Create a directory named 'arxiv' in the current directory and return its path."""
    save_dir = Path(current_dir) / 'arxiv'
    save_dir.mkdir(exist_ok=True)
    return save_dir

def get_paper(id):
    """Return the paper corresponding to the given id, or None if no paper was found."""
    res = arxiv.Search(id_list=[id], max_results=1).results()
    if not res:
        logging.warning(f"No arXiv paper found with id = {id}")
        return None
    return next(res)

def get_new_filename(paper, id):
    """Return a new filename based on the paper's author, title, and id."""
    author = paper.authors[0].name.split(' ')[-1]
    title = ''.join(re.sub(r'[^\w]',' ',paper.title).title().split(' ')[:3])
    return '_'.join([author, title, id]) + ".pdf"

def move_file(f, new_path):
    """Move the file to the new path."""
    f.rename(new_path)

def move_papers(current_dir):
    files = get_files(current_dir)
    save_dir = create_save_dir(current_dir)

    for f in files:
        id = f.stem # get arXiv id, remove ".pdf"
        if not re.match(r'\d{4}\.\d{5}(v\d+)?', id):
            logging.warning(f"Skipping file {f} because its name does not match the arXiv ID pattern")
            continue
        try:
            paper = get_paper(id)
            if paper is None:
                continue
            new_filename = get_new_filename(paper, id)
            new_path = save_dir / new_filename
            if new_path.exists():  # Check if the file already exists
                logging.info(f"File {new_path} already exists, deleting it.")
                new_path.unlink()  # Delete the file
            logging.info(f"Moving file to {new_path}")
            move_file(f, new_path)
        except arxiv.arxiv.HTTPError as e:
            logging.error(f"An error occurred while fetching the paper with id = {id}: {e}")