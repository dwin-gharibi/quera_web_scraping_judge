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
        scraper = SeleniumScraper("chrome")
        scraped_text = scraper.scrape_home_page()

        self.assertIsNotNone(scraped_text, "Failed to scrape the home page.")
        self.assertIn("Home Page", scraped_text, f"Scraped text '{scraped_text}' does not contain expected 'Home Page'.")

    def test_02_scrape_product_page(self):
        product_url = "http://nginx:80/product/1"
        scraper = SeleniumScraper("chrome")
        product_details = scraper.scrape_product_page(product_url)

        self.assertIsNotNone(product_details, "Failed to scrape product page.")
        self.assertIn("name", product_details, "Product name is missing in the scraped data.")
        self.assertIn("price", product_details, "Product price is missing in the scraped data.")
        self.assertIn("rating", product_details, "Product rating is missing in the scraped data.")

    def test_03_scrape_all_products(self):
        products_page_url = "http://nginx:80/products"
        scraper = SeleniumScraper("chrome")
        products = scraper.scrape_all_products(products_page_url)

        self.assertIsNotNone(products, "Failed to scrape products page.")
        self.assertGreater(len(products), 0, "No products were scraped.")
        for product in products:
            self.assertIn("name", product, "Product name is missing in the scraped data.")
            self.assertIn("price", product, "Product price is missing in the scraped data.")
            self.assertIn("rating", product, "Product rating is missing in the scraped data.")

    def test_04_scrape_invalid_page(self):
        invalid_url = "http://nginx:80/invalid_page"
        scraper = SeleniumScraper("chrome")
        result = scraper.scrape_home_page()

        self.assertIsNone(result, "Expected None when scraping an invalid page, but received content.")
        
    def test_05_check_browser_switch(self):
        chrome_scraper = SeleniumScraper("chrome")
        firefox_scraper = SeleniumScraper("firefox")
        
        chrome_title = chrome_scraper.scrape_home_page()
        firefox_title = firefox_scraper.scrape_home_page()

        self.assertIsNotNone(chrome_title, "Failed to scrape home page with Chrome.")
        self.assertIsNotNone(firefox_title, "Failed to scrape home page with Firefox.")
        self.assertEqual(chrome_title, firefox_title, "Titles from Chrome and Firefox do not match.")

if __name__ == "__main__":
    unittest.main()
