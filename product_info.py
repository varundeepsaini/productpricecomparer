import requests
from bs4 import BeautifulSoup


def extract_product_info_from_link(url):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36"}
        response = session.get(url, headers=headers)

        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('span', id="productTitle")
        product_price = soup.find('span', class_="a-price-whole")

        product_name = product_name.text.strip() if product_name else "Product name not found"
        product_price = product_price.text.strip() if product_price else "Product price not found"

        return product_name, product_price
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error: {e}")
        return None
