from playwright.sync_api import Page
from pages.base_page import BasePage

class CarPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "https://www.saucedemo.com/cart.html")
        self.inventory_items_names = page.locator('data-test="inventory-item-name"')
        self.checkout_button = page.locator('[data-test="checkout"]')
        
    def transform_product_name(self, product_name):
        return "remove-" + product_name.lower().replace(" ", "-")
    
    def remove_product_from_car(self, page: Page, product_name: str):
        product_locator = self.inventory_items_names.filter(has_text=product_name)
        if product_locator:
            remove_button = self.page.locator('[data-test="' + self.transform_product_name(product_name) + '"]')
            remove_button.click()