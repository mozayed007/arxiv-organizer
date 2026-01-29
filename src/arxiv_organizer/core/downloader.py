import arxiv
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from ..models import DownloadConfig, PaperMetadata, GlobalConfig
from ..utils.ai import GeminiClient

class ArxivDownloader:
    def __init__(self, config: GlobalConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        # Always instantiate, but it will be non-functional if no API key
        self.ai_client = GeminiClient(config.google_api_key)

    def download(self, download_config: DownloadConfig) -> List[Path]:
        query = self._construct_query(download_config)
        self.logger.info(f"Searching arXiv with query: {query}")

        try:
            search = arxiv.Search(
                query=query,
                max_results=download_config.max_results * 2, # Fetch more to allow for filtering
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            candidates = []
            for result in search.results():
                if self._filter_by_date(result, download_config.period):
                    candidates.append(self._to_metadata(result))
                    if len(candidates) >= download_config.max_results:
                        break
            
            self.logger.info(f"Found {len(candidates)} candidates after date filtering.")

            if download_config.smart_judge and download_config.judge_criteria:
                self.logger.info("Running Smart Judge...")
                accepted_ids = self.ai_client.judge_papers(candidates, download_config.judge_criteria)
                candidates = [p for p in candidates if p.id in accepted_ids]
                self.logger.info(f"Smart Judge accepted {len(candidates)} papers.")

            download_dir = Path(download_config.download_dir)
            download_dir.mkdir(parents=True, exist_ok=True)
            
            downloaded_files = []
            for paper_meta in tqdm(candidates, desc="Downloading"):
                path = self._download_paper(paper_meta, download_dir)
                if path:
                    downloaded_files.append(path)
            
            return downloaded_files

        except Exception as e:
            self.logger.error(f"Download process failed: {e}")
            return []

    def _construct_query(self, config: DownloadConfig) -> str:
        parts = []
        if config.query:
            parts.append(config.query)
        
        if config.keywords:
            parts.append(" OR ".join([f'all:"{k}"' for k in config.keywords]))
            
        if config.title_keywords:
            parts.append(" OR ".join([f'ti:"{k}"' for k in config.title_keywords]))
            
        if config.abstract_keywords:
            parts.append(" OR ".join([f'abs:"{k}"' for k in config.abstract_keywords]))
            
        return " AND ".join([f"({p})" for p in parts]) if parts else "all:electron" # Default fallback

    def _filter_by_date(self, result, period: str) -> bool:
        if period == "all":
            return True
            
        days_map = {
            "1d": 1, "7d": 7, "30d": 30, "90d": 90,
            "1y": 365, "3y": 365*3, "5y": 365*5, 
            "10y": 365*10, "20y": 365*20, "30y": 365*30
        }
        
        days = days_map.get(period)
        if not days:
            return True
            
        cutoff = datetime.now(result.published.tzinfo) - timedelta(days=days)
        return result.published >= cutoff

    def _to_metadata(self, result) -> PaperMetadata:
        return PaperMetadata(
            id=result.entry_id.split('/')[-1],
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

    def _download_paper(self, paper: PaperMetadata, directory: Path) -> Optional[Path]:
        try:
            # Use the paper ID as filename initially
            filename = f"{paper.id}.pdf"
            path = directory / filename
            
            if path.exists():
                return path
                
            paper_obj = next(arxiv.Search(id_list=[paper.id]).results())
            paper_obj.download_pdf(dirpath=str(directory), filename=filename)
            
            # Respect arXiv rate limit (1 req/3s)
            time.sleep(3)
            return path
        except Exception as e:
            self.logger.error(f"Failed to download {paper.id}: {e}")
            return None
