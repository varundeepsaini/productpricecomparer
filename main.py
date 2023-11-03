import requests
from bs4 import BeautifulSoup


def scrape_amazon_product(url):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/95.0.4638.69 Safari/537.36'}

    response = session.get(url, headers=headers)

    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    product_name = soup.find('span', id='productTitle')
    product_price = soup.find('span', class_='a-price-whole')

    if product_name is not None:
        product_name = product_name.text.strip()
    else:
        product_name = 'Product name not found'
    if product_price is not None:
        product_price = product_price.text.strip()
    else:
        product_price = 'Product price not found'
    return {'Product Name': product_name, 'Product Price': product_price}


if __name__ == '__main__':
    product_url = input('Enter Amazon Product URL: ')

    result = scrape_amazon_product(product_url)

    if result is not None:
        print(f"Product Name: {result['Product Name']}")
        print(f"Product Price: {result['Product Price']}")
    else:
        print('Error: Request failed or invalid URL')
