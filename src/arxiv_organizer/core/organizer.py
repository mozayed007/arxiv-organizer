import os
import shutil
from pathlib import Path
import re
import logging
import json
import time
import importlib.resources
import arxiv
from tqdm import tqdm
from datetime import datetime
from ..models import OrganizerConfig, GlobalConfig, PaperMetadata
from ..utils.ai import GeminiClient

class ArxivOrganizer:
    def __init__(self, config: OrganizerConfig, global_config: GlobalConfig):
        self.config = config
        self.global_config = global_config
        self.base_dir = Path(config.base_dir)
        self.arxiv_dir = self.base_dir / 'arxiv'
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self.categories_map = self._load_categories()
        self.library_file = self.arxiv_dir / 'library.json'
        self.library = self._load_library()
        
        # Always instantiate AI client (will be non-functional if no API key or smart_organize is False)
        self.ai_client = GeminiClient(global_config.google_api_key) if config.smart_organize else None

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _load_categories(self):
        try:
            categories_file = importlib.resources.files('arxiv_organizer').joinpath('utils', 'categories.json')
            if not categories_file.exists():
                 self.logger.warning("categories.json not found.")
                 return {}
            with open(categories_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load categories: {e}")
            return {}

    def _load_library(self):
        if self.library_file.exists():
            try:
                with open(self.library_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load library index: {e}")
        return {}

    def _save_library(self):
        try:
            with open(self.library_file, 'w') as f:
                json.dump(self.library, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save library index: {e}")

    def process(self):
        self.arxiv_dir.mkdir(exist_ok=True)
        
        # Find PDFs in base_dir, excluding the arxiv/ subdirectory
        all_pdfs = []
        for pdf in self.base_dir.glob("*.pdf"):
            if re.match(r'\d{4}\.\d{5}(v\d+)?\.pdf', pdf.name):
                all_pdfs.append(pdf)
        
        # Filter out already indexed papers if the file still exists
        new_pdfs = []
        for pdf in all_pdfs:
            paper_id = pdf.stem
            # Basic check: if ID is in library and file exists at recorded path
            if paper_id in self.library:
                recorded_path = Path(self.library[paper_id]['path'])
                if (self.arxiv_dir / recorded_path).exists():
                    continue
            new_pdfs.append(pdf)

        if not new_pdfs:
            self.logger.info("No new arXiv papers found to organize.")
            return

        self.logger.info(f"Found {len(new_pdfs)} new papers to process.")

        # Process in batches to respect rate limits
        batch_size = 50
        for i in range(0, len(new_pdfs), batch_size):
            batch = new_pdfs[i:i + batch_size]
            self._process_batch(batch)
            
            # Rate limit delay between batches (arXiv recommends 3s delay)
            if i + batch_size < len(new_pdfs):
                time.sleep(3)

        self._save_library()
        self.logger.info("Organization complete.")

    def _process_batch(self, pdf_batch: list[Path]):
        # Extract IDs
        paper_ids = [pdf.stem for pdf in pdf_batch]
        pdf_map = {pdf.stem: pdf for pdf in pdf_batch}
        
        try:
            # Fetch metadata for the whole batch
            search = arxiv.Search(id_list=paper_ids)
            results = list(search.results())
            
            for result in tqdm(results, desc="Processing Batch"):
                paper_id = result.entry_id.split('/')[-1]
                pdf_path = pdf_map.get(paper_id)
                
                if not pdf_path:
                    continue

                # Convert to Pydantic model
                paper = PaperMetadata(
                    id=paper_id,
                    title=result.title,
                    authors=[a.name for a in result.authors],
                    summary=result.summary,
                    published=result.published,
                    updated=result.updated,
                    primary_category=result.primary_category,
                    categories=result.categories,
                    pdf_url=result.pdf_url,
                    doi=result.doi
                )

                # Smart Features (Rate limited internally by GeminiClient)
                if self.ai_client:
                    analysis = self.ai_client.analyze_paper(paper, self.config.custom_topics)
                    paper.custom_topic = analysis.get('topic', 'Unclassified')
                    paper.ai_summary = analysis.get('summary')
                    paper.ai_tags = analysis.get('tags')

                # Rename
                new_filename = self._get_new_filename(paper, paper_id)
                new_path = self.arxiv_dir / new_filename
                
                if new_path.exists():
                    new_path.unlink()
                
                # Move to 'arxiv' folder first (renamed)
                shutil.move(str(pdf_path), str(new_path))

                # Organize into subcategory
                final_path = self._organize_into_category(new_path, paper)
                
                # Save sidecar
                self._save_metadata_sidecar(final_path, paper)

                # Update library
                self.library[paper_id] = {
                    'path': str(final_path.relative_to(self.arxiv_dir)),
                    'title': paper.title,
                    'authors': paper.authors,
                    'category': paper.primary_category,
                    'updated_at': datetime.now().isoformat(),
                    'ai_summary': paper.ai_summary,
                    'ai_tags': paper.ai_tags,
                    'custom_topic': paper.custom_topic
                }

        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")

    def _get_new_filename(self, paper: PaperMetadata, paper_id: str) -> str:
        author = paper.authors[0].split(' ')[-1]
        clean_title = ''.join(re.sub(r'[^\w]', ' ', paper.title).title().split(' ')[:3])
        return f"{author}_{clean_title}_{paper_id}.pdf"

    def _organize_into_category(self, file_path: Path, paper: PaperMetadata) -> Path:
        # Priority: Custom Topic > Arxiv Category
        if paper.custom_topic and paper.custom_topic != "Unclassified":
            dest_dir = self.arxiv_dir / "Smart_Topics" / paper.custom_topic
        else:
            category = paper.primary_category
            main_category = category.split('.')[0] if '.' in category else category
            folder_name = self.categories_map.get(main_category, {}).get(category, category)
            dest_dir = self.arxiv_dir / main_category / folder_name
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / file_path.name
        
        if dest_path.exists():
            file_path.unlink()
            return dest_path
        else:
            shutil.move(str(file_path), str(dest_path))
            return dest_path

    def _save_metadata_sidecar(self, pdf_path: Path, paper: PaperMetadata):
        sidecar_path = pdf_path.with_suffix('.json')
        with open(sidecar_path, 'w') as f:
            f.write(paper.model_dump_json(indent=2))
