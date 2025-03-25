import unittest
import time
from scripts.docker_handler import DockerHandler
from solution.solution import SeleniumScraper

class TestSeleniumScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DockerHandler.start_container()
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        DockerHandler.stop_container()

    def test_01_scrape_home_page(self):
        scraper = SeleniumScraper("firefox")
        scraped_text = scraper.scrape_home_page()

        self.assertIsNotNone(scraped_text, "Failed to scrape the home page.")
        self.assertIn("Home Page", scraped_text, f"Scraped text '{scraped_text}' does not contain expected 'Home Page'.")

    def test_02_scrape_product_page(self):
        product_url = "http://nginx:80/product_page.html"
        scraper = SeleniumScraper("firefox")
        product_details = scraper.scrape_product_page(product_url)

        self.assertIsNotNone(product_details, "Failed to scrape product page.")
        self.assertIn("name", product_details, "Product name is missing in the scraped data.")
        self.assertIn("price", product_details, "Product price is missing in the scraped data.")
        self.assertIn("rating", product_details, "Product rating is missing in the scraped data.")

    def test_03_scrape_all_products(self):
        products_page_url = "http://nginx:80/products_page.html"
        scraper = SeleniumScraper("firefox")
        products = scraper.scrape_all_products(products_page_url)

        self.assertIsNotNone(products, "Failed to scrape products page.")
        self.assertGreater(len(products), 0, "No products were scraped.")
        for product in products:
            self.assertIn("name", product, "Product name is missing in the scraped data.")
            self.assertIn("price", product, "Product price is missing in the scraped data.")
            self.assertIn("rating", product, "Product rating is missing in the scraped data.")

    def test_04_scrape_invalid_page(self):
        invalid_url = "http://nginx:80/invalid_pag"
        scraper = SeleniumScraper("firefox")
        result = scraper.scrape_product_page(invalid_url)

        self.assertIsNone(result, "Expected None when scraping an invalid page, but received content.")
        
if __name__ == "__main__":
    unittest.main()
