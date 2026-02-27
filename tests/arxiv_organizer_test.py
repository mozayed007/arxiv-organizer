import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
import tempfile
import json
from pathlib import Path
from datetime import datetime, timezone

from arxiv_organizer.core.organizer import ArxivOrganizer
from arxiv_organizer.models import OrganizerConfig, GlobalConfig


class TestArxivOrganizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create configs
        self.global_config = GlobalConfig(google_api_key=None)
        self.organizer_config = OrganizerConfig(
            base_dir=str(self.test_dir),
            smart_organize=False,
            custom_topics=None
        )
        
        # Create organizer
        self.organizer = ArxivOrganizer(self.organizer_config, self.global_config)
        
        # Create a dummy PDF matching arXiv ID pattern
        self.pdf_path = self.test_dir / "2101.00001.pdf"
        self.pdf_path.touch()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    @patch('arxiv_organizer.core.organizer.arxiv.Search')
    def test_process_organizes_paper(self, mock_search):
        """Test that process() organizes papers correctly."""
        # Mock arXiv response
        mock_result = MagicMock()
        mock_result.entry_id = "http://arxiv.org/abs/2101.00001"
        mock_result.title = "Test Paper Title"
        mock_result.authors = [MagicMock(name="John Doe")]
        mock_result.authors[0].name = "John Doe"
        mock_result.primary_category = "cs.AI"
        mock_result.categories = ["cs.AI"]
        mock_result.summary = "This is a test abstract."
        mock_result.published = datetime.now(timezone.utc)
        mock_result.updated = datetime.now(timezone.utc)
        mock_result.pdf_url = "http://arxiv.org/pdf/2101.00001"
        mock_result.doi = None
        
        mock_search.return_value.results.return_value = [mock_result]

        # Mock categories map
        self.organizer.categories_map = {'cs': {'cs.AI': 'Artificial Intelligence'}}

        # Run the organizer
        self.organizer.process()

        # Verify the arxiv directory was created
        arxiv_dir = self.test_dir / "arxiv"
        self.assertTrue(arxiv_dir.exists(), "arxiv directory should be created")

        # Check if library.json was created
        library_path = arxiv_dir / "library.json"
        self.assertTrue(library_path.exists(), "library.json should be created")
        
        # Verify library content
        with open(library_path, 'r') as f:
            library = json.load(f)
            self.assertIn("2101.00001", library)
            self.assertEqual(library["2101.00001"]["title"], "Test Paper Title")

    @patch('arxiv_organizer.core.organizer.arxiv.Search')
    def test_process_skips_already_indexed(self, mock_search):
        """Test that already indexed papers are skipped."""
        # Create arxiv directory and library with existing entry
        arxiv_dir = self.test_dir / "arxiv"
        arxiv_dir.mkdir()
        
        # Create a fake organized file
        organized_dir = arxiv_dir / "cs" / "Artificial Intelligence"
        organized_dir.mkdir(parents=True)
        organized_file = organized_dir / "Doe_TestPaperTitle_2101.00001.pdf"
        organized_file.touch()
        
        # Create library index with existing entry
        library = {
            "2101.00001": {
                "path": "cs/Artificial Intelligence/Doe_TestPaperTitle_2101.00001.pdf",
                "title": "Test Paper Title",
                "authors": ["John Doe"],
                "category": "cs.AI",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
        with open(arxiv_dir / "library.json", 'w') as f:
            json.dump(library, f)
        
        # Reload organizer to pick up library
        self.organizer = ArxivOrganizer(self.organizer_config, self.global_config)
        
        # Run process
        self.organizer.process()
        
        # The search should not have been called for already indexed papers
        mock_search.assert_not_called()


class TestOrganizerConfig(unittest.TestCase):
    def test_default_config(self):
        """Test default configuration values."""
        config = OrganizerConfig(base_dir=".")
        self.assertEqual(config.base_dir, ".")
        self.assertFalse(config.smart_organize)
        self.assertIsNone(config.custom_topics)

    def test_custom_topics_config(self):
        """Test configuration with custom topics."""
        config = OrganizerConfig(
            base_dir="./papers",
            smart_organize=True,
            custom_topics=["Agents", "RAG", "Multimodal"]
        )
        self.assertTrue(config.smart_organize)
        self.assertEqual(len(config.custom_topics), 3)


if __name__ == '__main__':
    unittest.main()
