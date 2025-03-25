import unittest
import os
from scripts.docker_handler import DockerHandler
from scripts.selenium_runner import AssemblyRunner
from solution.solution import SeleniumScraper

class TestAssemblyPrograms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DockerHandler.start_container()

    # @classmethod
    # def tearDownClass(cls):
    #     DockerHandler.stop_container()

    def test_01_scrape_home_page(self):
        """Test the solution.py script functionality (scraping home page)."""
        scraper = SeleniumScraper("chrome")
        scraped_text = scraper.scrape_home_page()

        # Verify that we have successfully scraped the text and it matches the expected content
        self.assertIsNotNone(scraped_text, "Failed to scrape the home page.")
        self.assertIn("Home Page", scraped_text, f"Scraped text '{scraped_text}' does not contain expected 'Home Page'.")

if __name__ == "__main__":
    unittest.main()
