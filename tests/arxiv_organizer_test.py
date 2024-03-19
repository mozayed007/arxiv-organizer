import unittest
import os
import argparse
from arxiv_organizer import process_papers

class TestArxivOrganizer(unittest.TestCase):
    def setUp(self):
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Test the arXiv organizer.')
        parser.add_argument('--dir', type=str, default=os.getcwd(), help='The directory containing the papers to process.')
        args = parser.parse_args()

        # Use the given directory or the current directory if no directory was given
        self.test_folder = args.dir

    def test_process_papers(self):
        # Call the function with the test folder
        process_papers(self.test_folder, scrape=True)

        # Check if the 'arxiv' folder was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, 'arxiv')))

        # Traverse through the 'arxiv' directory and its subdirectories
        found_pdf = False
        for root, dirs, files in os.walk(os.path.join(self.test_folder, 'arxiv')):
            # If any PDF file is found, set the flag to True
            if any(fname.endswith('.pdf') for fname in files):
                found_pdf = True
                break

        # If no PDF file is found after traversing all directories, the test fails
        if not found_pdf:
            self.fail("No PDF files found in 'arxiv' directory or its subdirectories")

if __name__ == '__main__':
    unittest.main()