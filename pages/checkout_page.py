from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckOutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "https://www.saucedemo.com/checkout-step-one.html")
        self.first_name_field = page.locator('[data-test="firstName"]')
        self.last_name_field = page.locator('[data-test=lastName]')
        self.postal_code_field = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.your_car_item = page.locator('[data-test="inventory-item"]')
        self.error_message = page.locator('[data-test="error"]')
        
       
    def get_product_price(self, page: Page, product_name: str):
        # Busca el producto en la lista de productos
        product_locator = self.your_car_item.filter(has_text=product_name).first
        
         # Si el producto existe, retorna el precio
        if product_locator:
            price = product_locator.locator('[data-test="inventory-item-price"]').inner_text()
            return price 
        else:
            self.logger.info(f"Producto '{product_name}' no encontrado")