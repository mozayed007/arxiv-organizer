"""
Verification script to test the refactored arxiv-organizer package.
Run this after making changes to verify the package works correctly.
"""
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import shutil
import tempfile
import json
from datetime import datetime, timezone

from arxiv_organizer.core.organizer import ArxivOrganizer
from arxiv_organizer.core.downloader import ArxivDownloader
from arxiv_organizer.models import OrganizerConfig, GlobalConfig, DownloadConfig, PaperMetadata


class TestRefactoredOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.global_config = GlobalConfig(google_api_key=None)
        self.organizer_config = OrganizerConfig(
            base_dir=str(self.test_dir),
            smart_organize=False,
            custom_topics=None
        )
        self.organizer = ArxivOrganizer(self.organizer_config, self.global_config)
        
        # Create a dummy PDF
        self.pdf_path = self.test_dir / "2101.00001.pdf"
        self.pdf_path.touch()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('arxiv_organizer.core.organizer.arxiv.Search')
    def test_process_paper(self, mock_search):
        # Mock arxiv response
        mock_result = MagicMock()
        mock_result.entry_id = "http://arxiv.org/abs/2101.00001"
        mock_result.title = "Test Paper Title"
        mock_result.authors = [MagicMock(name="John Doe")]
        mock_result.authors[0].name = "John Doe"
        mock_result.primary_category = "cs.AI"
        mock_result.categories = ["cs.AI"]
        mock_result.summary = "Abstract"
        mock_result.published = datetime.now(timezone.utc)
        mock_result.updated = datetime.now(timezone.utc)
        mock_result.pdf_url = "http://arxiv.org/pdf/2101.00001"
        mock_result.doi = None
        
        mock_search.return_value.results.return_value = [mock_result]

        # Mock categories map to ensure we have a mapping
        self.organizer.categories_map = {'cs': {'cs.AI': 'Artificial Intelligence'}}

        self.organizer.process()

        # Check if file was moved and renamed
        expected_filename = "Doe_TestPaperTitle_2101.00001.pdf"
        expected_path = self.test_dir / "arxiv" / "cs" / "Artificial Intelligence" / expected_filename
        
        self.assertTrue(expected_path.exists(), f"File not found at {expected_path}")

        # Check sidecar
        sidecar_path = expected_path.with_suffix('.json')
        self.assertTrue(sidecar_path.exists(), "Sidecar file not created")
        
        with open(sidecar_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['title'], "Test Paper Title")

        # Check library index
        library_path = self.test_dir / "arxiv" / "library.json"
        self.assertTrue(library_path.exists(), "Library index not created")
        
        with open(library_path, 'r') as f:
            library = json.load(f)
            self.assertIn("2101.00001", library)
            self.assertEqual(library["2101.00001"]["title"], "Test Paper Title")


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.global_config = GlobalConfig(google_api_key=None)
        self.downloader = ArxivDownloader(self.global_config)

    def test_construct_query_keywords(self):
        config = DownloadConfig(
            keywords=["machine learning", "neural networks"],
            period="30d",
            max_results=10
        )
        query = self.downloader._construct_query(config)
        self.assertIn('all:"machine learning"', query)
        self.assertIn('all:"neural networks"', query)

    def test_construct_query_title_keywords(self):
        config = DownloadConfig(
            title_keywords=["attention"],
            period="7d",
            max_results=5
        )
        query = self.downloader._construct_query(config)
        self.assertIn('ti:"attention"', query)


class TestModels(unittest.TestCase):
    def test_paper_metadata(self):
        paper = PaperMetadata(
            id="2101.00001",
            title="Test Paper",
            authors=["John Doe", "Jane Smith"],
            summary="Test abstract",
            published=datetime.now(timezone.utc),
            updated=datetime.now(timezone.utc),
            primary_category="cs.AI",
            categories=["cs.AI", "cs.LG"],
            pdf_url="http://arxiv.org/pdf/2101.00001"
        )
        self.assertEqual(paper.id, "2101.00001")
        self.assertEqual(len(paper.authors), 2)
        self.assertIsNone(paper.ai_summary)
        self.assertIsNone(paper.custom_topic)


if __name__ == '__main__':
    unittest.main(verbosity=2)
