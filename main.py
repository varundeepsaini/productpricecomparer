import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


class ShoppingCart:
    def __init__(self):
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)

    def print_cart(self):
        if not self.cart:
            print("Your cart is empty.")
        else:
            print("Shopping Cart:")
            for idx, product in enumerate(self.cart, start=1):
                print(f"{idx}. Product Name: {product['name']}")
                print(f"   Price: {product['price']}\n")


def search_amazon_product(product_name):
    try:
        base_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'

        session = requests.Session()
        headers = Headers(headers=True).generate()
        session.headers.update(headers)

        response = session.get(base_url)

        response.raise_for_status()  # Raise an error if the request fails

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        for result in soup.find_all("div", {"data-component-type": "s-search-result"}):
            title = result.find('h2').text.strip()
            price = result.find("span", class_="a-offscreen")
            if price:
                price = price.text.strip()
            else:
                price = "Not available"

            products.append({"name": title, "price": price})

        return products
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def extract_product_info_from_link(url):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36"}
        response = session.get(url, headers=headers)

        response.raise_for_status()  # Raise an error if the request fails

        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('span', id="productTitle")
        product_price = soup.find('span', class_="a-price-whole")

        product_name = product_name.text.strip() if product_name else "Product name not found"
        product_price = product_price.text.strip() if product_price else "Product price not found"

        return {"name": product_name, "price": product_price}
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error: {e}")
        return None


def display_search_results(product_list):
    if not product_list:
        print("No results found.")
    else:
        print("Top 5 search results on Amazon:")
        for idx, product in enumerate(product_list, start=1):
            print(f"{idx}. Product Name: {product['name']}")
            print(f"   Price: {product['price']}\n")


def main():
    cart = ShoppingCart()
    while True:
        print("1. Search for a product")
        print("2. Add a product by link")
        print("3. Print the cart")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            product_name = input("Enter the name of the product you want to search on Amazon: ")
            product_list = search_amazon_product(product_name)[:5]
            display_search_results(product_list)

            try:
                selection = int(input("Select a product (enter the number): "))
                if 1 <= selection <= len(product_list):
                    selected_product = product_list[selection - 1]
                    cart.add_to_cart(selected_product)
                    print("Product added to the cart.")
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "2":
            product_link = input("Enter the Amazon product link: ")
            product_info = extract_product_info_from_link(product_link)
            if product_info:
                cart.add_to_cart(product_info)
                print("Product added to the cart.")
            else:
                print("Failed to extract product information from the provided link.")

        elif choice == "3":
            cart.print_cart()

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
