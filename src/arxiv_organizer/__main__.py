import argparse
import os
from pathlib import Path
from .core.organizer import ArxivOrganizer
from .core.downloader import ArxivDownloader
from .models import GlobalConfig, DownloadConfig, OrganizerConfig
from .utils import categories

def process_papers():
    parser = argparse.ArgumentParser(description='Organize and Download arXiv papers.')
    
    # General
    parser.add_argument('--directory', type=str, default='.', help='Directory to process or download to')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to .env file')
    parser.add_argument('--update-categories', action='store_true', help='Update arXiv categories taxonomy')

    # Download
    parser.add_argument('--download', action='store_true', help='Enable download mode')
    parser.add_argument('--query', type=str, help='Raw arXiv query')
    parser.add_argument('--keywords', type=str, help='Comma-separated keywords')
    parser.add_argument('--title-keywords', type=str, help='Comma-separated title keywords')
    parser.add_argument('--abstract-keywords', type=str, help='Comma-separated abstract keywords')
    parser.add_argument('--period', type=str, default='all', help='Time period (1d, 7d, 30d, 1y, etc.)')
    parser.add_argument('--max', type=int, default=10, help='Max papers to download')
    parser.add_argument('--smart-judge', action='store_true', help='Enable Gemini Smart Judge')
    parser.add_argument('--judge-criteria', type=str, help='Criteria for Smart Judge')

    # Organization
    parser.add_argument('--smart-organize', action='store_true', help='Enable AI-based organization and enrichment')
    parser.add_argument('--custom-topics', type=str, help='Comma-separated custom topics for classification')

    args = parser.parse_args()

    # Load Config
    global_config = GlobalConfig(_env_file=args.env_file)

    if args.update_categories:
        if hasattr(args, 'download') and args.download:
            print("Warning: --update-categories ignores all other flags.")
        categories.update_categories()
        return

    base_dir = Path(args.directory).resolve()

    # Download Phase
    if args.download:
        download_config = DownloadConfig(
            query=args.query,
            keywords=args.keywords.split(',') if args.keywords else None,
            title_keywords=args.title_keywords.split(',') if args.title_keywords else None,
            abstract_keywords=args.abstract_keywords.split(',') if args.abstract_keywords else None,
            period=args.period,
            max_results=args.max,
            smart_judge=args.smart_judge,
            judge_criteria=args.judge_criteria,
            download_dir=str(base_dir)
        )
        
        downloader = ArxivDownloader(global_config)
        downloaded = downloader.download(download_config)
        if not downloaded:
            print("No papers downloaded.")
            return
        print(f"Downloaded {len(downloaded)} papers.")

    # Organize Phase
    organizer_config = OrganizerConfig(
        base_dir=str(base_dir),
        smart_organize=args.smart_organize,
        custom_topics=args.custom_topics.split(',') if args.custom_topics else None
    )
    
    organizer = ArxivOrganizer(organizer_config, global_config)
    organizer.process()

if __name__ == '__main__':
    process_papers()