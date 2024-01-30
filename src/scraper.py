import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ScrapeLazada():
    """
    A class used to scrape product data from Lazada website.
    """

    def get_rating(self, rating_div):
        """Extracts and calculates the average rating from a given div element."""
        if not rating_div:
            return 0.0  # Return 0.0 for items with no rating

        full_stars = len(rating_div.find_all('i', class_='_9-ogB Dy1nx'))
        partial_star_class = rating_div.find(
            'i', class_=lambda x: x != '_9-ogB Dy1nx' and x != '_9-ogB W1iJ5')

        partial_star_values = {
            'TZlP8': 0.3,
            # Additional mappings can be added here
        }

        partial_star_value = partial_star_values.get(
            partial_star_class['class'][1], 0) if partial_star_class else 0
        return full_stars + partial_star_value

    def extract_price(self, item):
        """Extracts and converts price to float."""
        price_text = item.find('span', class_='ooOxS').text.replace('₫', '').replace('.', '').replace(' ', '')
        return float(price_text) if price_text else 0.0

    def extract_reviews(self, item):
        """Extracts and converts total number of reviews to int."""
        reviews_span = item.find('span', class_='qzqFw')
        reviews_text = reviews_span.text.strip("()") if reviews_span else '0'
        return int(reviews_text)

    def extract_sold(self, item):
        """
        Extracts and converts the number of items sold to an integer. 
        Handles different formats including '100 sold', '100 đã bán', '1k+ sold', and '1k+ đã bán'.
        """
        sold_info = item.find('span', class_='_1cEkb')
        if sold_info and sold_info.span:
            sold_text = sold_info.span.get_text(strip=True)
            if 'k+' in sold_text:
                # Handle 'k+' notation by converting it to thousands
                sold_number = float(re.findall(r'\d+', sold_text)[0]) * 1000
            else:
                # Extract the numeric part for regular numbers
                sold_numbers = re.findall(r'\d+', sold_text)
                sold_number = int(sold_numbers[0]) if sold_numbers else 0
            return int(sold_number)
        return 0

    def extract_sale_info(self, item):
        """
        Extracts the sale information.
        Keeps only the percentage figure, removes 'off' text, and defaults to '0%' if there is no sale.
        """
        sale_info_div = item.find('div', class_='WNoq3')
        if sale_info_div and sale_info_div.span:
            sale_text = sale_info_div.span.get_text(strip=True)
            # Extract percentage using regular expression
            percentage = re.findall(r'\d+%', sale_text)
            return percentage[0] if percentage else '0%'
        return '0%'

    def scrape(self):
        """Scrapes product data from Lazada and saves it to an Excel file."""
        url = 'https://www.lazada.vn/catalog/?spm=a2o4n.searchlistcategory.search.d_go.2099564f46GQyC&q=l%C4%83n%20n%C3%A1ch'
        total_pages = 56
        driver = webdriver.Chrome()
        driver.get(url)

        products = []
        for i in range(total_pages):
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            for item in soup.findAll('div', class_="Bm3ON"):
                product_name = item.find('div', class_='RfADt').text
                location = item.find('span', class_='oa6ri').text
                price = self.extract_price(item)
                rating = self.get_rating(item.find('div', class_='mdmmT _32vUv'))
                reviews = self.extract_reviews(item)
                sold = self.extract_sold(item)
                sale_info = self.extract_sale_info(item)

                products.append((product_name, price, location, rating, reviews, sold, sale_info))

            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, ".ant-pagination-next > button").click()
            time.sleep(3)

        df = pd.DataFrame(products, columns=['Product Name', 'Price', 'Location', 'Average Rating', 'Total Reviews', 'Items Sold', 'Sale Info'])
        df.to_excel("out.xlsx", index=False)
        print('Data saved in local disk')
        driver.close()


def main():
    """Main function to initialize and run the Lazada scraper."""
    scraper = ScrapeLazada()
    scraper.scrape()


if __name__ == "__main__":
    main()
