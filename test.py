from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdNabuStoreTest:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    def open_store(self):
        self.driver.get("https://adnabu-store-assignment1.myshopify.com")
        self.driver.maximize_window()

    def login_store(self):
        password_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        password_input.send_keys("AdNabuQA")
        password_input.send_keys(Keys.RETURN)

    def search_product(self, product_name):

        search_icon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "summary[aria-label='Search']"))
        )
        search_icon.click()

        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
        )

        search_box.clear()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
    
    def open_first_product(self):

        # wait for search results page
        self.wait.until(
            EC.url_contains("/search")
        )

        # wait for products
        products = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#product-grid li")
            )
        )

        first_product = products[0].find_element(By.TAG_NAME, "a")

        # scroll to element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", first_product
        )

        # click using javascript (avoids overlay issues)
        self.driver.execute_script(
            "arguments[0].click();", first_product
        )
        
    def add_to_cart(self):
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "add"))
        )
        add_button.click()

    from datetime import datetime

    def verify_cart(self):

        # wait for cart drawer to appear
        cart_drawer = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "cart-drawer"))
        )

        status = "PASS"
        message = "Product successfully added to cart"

        print(message)

        with open("test_report.txt", "w") as report:
            report.write("Test Case: Search product and add to cart\n")
            report.write(f"Status: {status}\n")
            report.write(f"Message: {message}\n")

    def close(self):
        self.driver.quit()


def test_search_and_add_to_cart():
    test = AdNabuStoreTest()

    test.open_store()
    test.login_store()
    test.search_product("multi")
    test.open_first_product()
    test.add_to_cart()
    test.verify_cart()

    test.close()


if __name__ == "__main__":
    test_search_and_add_to_cart()
                   