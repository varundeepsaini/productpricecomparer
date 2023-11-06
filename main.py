import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, \
    QListWidget, QWidget, QLabel, QMessageBox


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


class ShoppingCartApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cart = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Shopping Cart')
        self.setGeometry(100, 100, 600, 400)

        self.search_entry = QLineEdit(self)
        self.search_button = QPushButton('Search', self)
        self.product_list = QListWidget(self)
        self.add_to_cart_button = QPushButton('Add to Cart', self)
        self.cart_text = QTextEdit(self)
        self.cart_label = QLabel("Shopping Cart:", self)

        self.link_entry = QLineEdit(self)
        self.add_link_button = QPushButton('Add by Link', self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(self.search_button)

        link_layout = QHBoxLayout()
        link_layout.addWidget(self.link_entry)
        link_layout.addWidget(self.add_link_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.product_list)
        main_layout.addWidget(self.add_to_cart_button)
        main_layout.addWidget(self.cart_label)
        main_layout.addWidget(self.cart_text)
        main_layout.addLayout(link_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.search_button.clicked.connect(self.search_product)
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.add_link_button.clicked.connect(self.add_product_by_link)

    def add_to_cart(self):
        selected_item = self.product_list.currentItem()
        if selected_item:
            product_name = selected_item.text()
            self.cart.append(product_name)
            self.update_cart_text()

    def search_amazon_product(self, product_name):
        base_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36'}
        response = requests.get(base_url, headers=headers)

        if response.status_code != 200:
            print("Error: Unable to access Amazon. Please try again later.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        for result in soup.find_all("div", {"data-component-type": "s-search-result"}):
            title = result.find('h2').text.strip()
            price = result.find("span", class_="a-offscreen")
            if price:
                price = price.text.strip()
            else:
                price = "Not available"

            products.append([title, price])

        return products

    def add_product_by_link(self):
        product_link = self.link_entry.text()
        product_name, product_price = extract_product_info_from_link(product_link)
        if product_name and product_price:
            self.cart.append(f"{product_name} - {product_price}")
            self.update_cart_text()
        else:
            self.show_error_message("Error", "Failed to extract product information from the provided link.")

    def update_cart_text(self):
        cart_text = "Shopping Cart:\n"
        for idx, item in enumerate(self.cart, start=1):
            cart_text += f"{idx}. {item[2::]}\n"
        self.cart_text.setPlainText(cart_text)

    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def search_product(self):
        product_name = self.search_entry.text()
        product_list = self.search_amazon_product(product_name)[:5]

        if not product_list:
            self.show_error_message("No Results", "No results found.")
        else:
            self.product_list.clear()
            for idx, (product_name, price) in enumerate(product_list, start=1):
                item_text = f"{idx}. {product_name} - {price}\n"
                self.product_list.addItem(item_text)


def main():
    app = QApplication(sys.argv)
    window = ShoppingCartApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
