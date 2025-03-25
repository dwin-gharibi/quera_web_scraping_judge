from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

class SeleniumScraper:
    def __init__(self, browser):
        options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.FirefoxOptions()
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options
        )
    
    def scrape_home_page(self):
        try:
            self.driver.get("http://nginx:80")
            time.sleep(2)
            
            element = self.driver.find_element(By.CLASS_NAME, "home-page-title")
            return element.text
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        
        finally:
            self.driver.quit()

    def scrape_product_page(self, product_url):
        try:
            self.driver.get(product_url)
            time.sleep(2)
            
            name = self.driver.find_element(By.CLASS_NAME, "product-name").text
            price = self.driver.find_element(By.CLASS_NAME, "product-price").text
            rating = self.driver.find_element(By.CLASS_NAME, "product-rating").text
            
            return {
                "name": name,
                "price": price,
                "rating": rating
            }
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        
        finally:
            self.driver.quit()

    def scrape_all_products(self, products_page_url):
        try:
            self.driver.get(products_page_url)
            time.sleep(2)
            
            product_elements = self.driver.find_elements(By.CLASS_NAME, "product")
            
            product_data = []
            
            for product in product_elements:
                try:
                    name = product.find_element(By.CLASS_NAME, "product-name").text
                    price = product.find_element(By.CLASS_NAME, "product-price").text
                    rating = product.find_element(By.CLASS_NAME, "product-rating").text
                    
                    product_data.append({
                        "name": name,
                        "price": price,
                        "rating": rating
                    })
                except Exception as e:
                    print(f"Error scraping product: {e}")
            
            return product_data
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        
        finally:
            self.driver.quit()
