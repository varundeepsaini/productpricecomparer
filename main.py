import requests
from bs4 import BeautifulSoup

def scrape_flipkart_product(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            print("Error: Request to Flipkart failed with status code", response.status_code)
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        product_name = soup.find('span', class_='B_NuCI')
        product_price = soup.find('div', class_='_30jeq3 _16Jk6d')

        if product_name is not None:
            product_name = product_name.text.strip()
        else:
            product_name = 'Product name not found'
        if product_price is not None:
            product_price = product_price.text.strip()
        else:
            product_price = 'Product price not found'
        return {'Product Name': product_name, 'Product Price': product_price}
    except Exception as e:
        print("Error:", e)
        return None

def scrape_amazon_product(url):
    try:
        session = requests.Session()
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        response = session.get(url, headers=headers)

        if response.status_code != 200:
            print("Error: Request to Amazon failed with status code", response.status_code)
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('span', id="productTitle")
        product_price = soup.find('span', class_="a-price-whole")

        if product_name is not None:
            product_name = product_name.text.strip()
        else:
            product_name = "Product name not found"
        if product_price is not None:
            product_price = product_price.text.strip()
        else:
            product_price = "Product price not found"
        return {'Product Name': product_name, 'Product Price': product_price}
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == '__main__':
    try:
        operations = int(input("Enter the website you want to scrape: \n1. Amazon\n2. Flipkart\n"))
        result = None
        if operations == 1:
            product_url = input('Enter Amazon Product URL: ')
            result = scrape_amazon_product(product_url)
        elif operations == 2:
            product_url = input('Enter Flipkart Product URL: ')
            result = scrape_flipkart_product(product_url)

        if result is not None:
            print(f"Product Name: {result['Product Name']}")
            print(f"Product Price: {result['Product Price']}")
        else:
            print('Error: Request failed or invalid URL')
    except ValueError:
        print("Error: Invalid input. Please enter 1 or 2 for website selection.")
