import re
from pathlib import Path
import arxiv # python wrapper for arxiv api
import logging

logging.basicConfig(level=logging.INFO)

def get_files(current_dir: Path) -> list:
    """Return a list of PDF files in the current directory whose names match the arXiv ID pattern."""
    return [pdf for pdf in current_dir.rglob("*.pdf") if re.match(r'\d{4}\.\d{5}(v\d+)?.pdf', pdf.name)]

def create_save_dir(current_dir: Path) -> Path:
    """Create a directory named 'arxiv' in the current directory and return its path."""
    save_dir = current_dir / 'arxiv'
    save_dir.mkdir(exist_ok=True)
    return save_dir

def get_paper(paper_id: str):
    """Return the paper corresponding to the given id, or None if no paper was found."""
    res = arxiv.Search(id_list=[paper_id], max_results=1).results()
    if not res:
        logging.warning(f"No arXiv paper found with id = {paper_id}")
        return None
    return next(res)

def get_new_filename(paper, paper_id: str) -> str:
    """Return a new filename based on the paper's author, title, and id."""
    author = paper.authors[0].name.split(' ')[-1]
    title = ''.join(re.sub(r'[^\w]', ' ', paper.title).title().split(' ')[:3])
    return f"{author}_{title}_{paper_id}.pdf"

def move_file(file: Path, new_path: Path):
    """Move the file to the new path."""
    file.rename(new_path)

def move_papers(current_dir: Path):
    files = get_files(current_dir)
    save_dir = create_save_dir(current_dir)

    for file in files:
        paper_id = file.stem  # get arXiv id, remove ".pdf"
        if not re.match(r'\d{4}\.\d{5}(v\d+)?', paper_id):
            logging.warning(f"Skipping file {file} because its name does not match the arXiv ID pattern")
            continue
        try:
            paper = get_paper(paper_id)
            if paper is None:
                continue
            new_filename = get_new_filename(paper, paper_id)
            new_path = save_dir / new_filename
            if new_path.exists():
                logging.info(f"File {new_path} already exists, deleting it.")
                new_path.unlink()
            logging.info(f"Moving file to {new_path}")
            move_file(file, new_path)
        except arxiv.arxiv.HTTPError as e:
            logging.error(f"An error occurred while fetching the paper with id = {paper_id}: {e}")