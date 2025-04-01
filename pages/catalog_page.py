from playwright.sync_api import Page
from pages.base_page import BasePage

class CatalogPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, "https://www.saucedemo.com/inventory.html")
        self.add_to_cart_button = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
        self.inventory_item_name = page.locator('[data-test="inventory-item-name"]') 
        self.inventory_item_description = page.locator('[data-test="inventory-item-description"]')
        self.inventory_item_price = page.locator('[data-test="inventory-item-price"]') 
        self.product_sort_container = page.locator('[data-test="product-sort-container"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.product_price = page.locator('[data-test="inventory-item-price"]') 
        self.hamburger_menu = page.get_by_text("Open Menu")
        self.logout_button = page.locator('[data-test="logout-sidebar-link"]')
        
    def click_product_sort(self, page: Page, option: str):
        self.product_sort_container.click()
        self.product_sort_container.select_option(value=option)
        
    def get_list_products_name(self, list_products):
        list_products_final = []        
        for product in list_products:    
            list_products_final.append(product.text_content())
        return list_products_final
    
    def add_to_car(self, page: Page, product_name: str):
        # Busca el producto en la lista de productos
        product_locator = self.inventory_item_name.filter(has_text=product_name).first
             

        # Si el producto existe, agrega al carrito
        if product_locator:
            add_to_cart_button = self.page.locator(
                '[data-test="' + self.transform_product_name(product_name) + '"]'
            )
            add_to_cart_button.click(timeout=self.timeout)
            self.logger.info(f"Producto '{product_name}' agregado al carrito")
        else:
            self.logger.info(f"Producto '{product_name}' no encontrado")

    def transform_product_name(self, product_name):
        return "add-to-cart-" + product_name.lower().replace(" ", "-")
    
    def get_product_price(self, page: Page, product_name: str):
        # Busca el producto en la lista de productos
        product_locator = self.inventory_item_description.filter(has_text=product_name).first
        
         # Si el producto existe, retorna el precio
        if product_locator:
            price = product_locator.locator('[data-test="inventory-item-price"]').inner_text()
            return price 
        else:
            self.logger.info(f"Producto '{product_name}' no encontrado")