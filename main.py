import requests
from bs4 import BeautifulSoup


def scrape_amazon_product(url):
    req = requests.get(url)
    if req.status_code != 200:
        return {None: None}

    soup = BeautifulSoup(req.text, 'html.parser')

    product_name = (soup.find('span', {'id': 'productTitle'}).get_text().strip())
    product_price = soup.find('span', {'id': 'priceblock_ourprice'}).get_text().strip()

    data = {"Product Name": product_name, "Product Price": product_price}
    return data


if __name__ == "__main__":
    product_url = input("Enter Amazon Product URL: ")
    result = scrape_amazon_product(product_url)

    if list(result.keys())[0] is None:
        print("Error: Request failed")
    else:
        for key, value in result.items():
            print(f"{key}: {value}")

