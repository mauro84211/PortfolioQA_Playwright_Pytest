import pytest
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage
from pages.car_page import CarPage

@pytest.mark.parametrize("product_name", [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt"
])
def test_add_product_to_cart(logged_in_app: Page, product_name: str):   
      
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, product_name)    
    expect(catalog_page.cart_link).to_have_text("1") 
       
    catalog_page.cart_link.click()
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/cart.html")
    
    car_page = CarPage(logged_in_app)  
             
    assert car_page.inventory_items_names.filter(has_text=product_name) is not None
    car_page.remove_product_from_car(logged_in_app, product_name)
    
def test_multiple_product_to_car(logged_in_app: Page):
    
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, "Sauce Labs Backpack")    
    catalog_page.add_to_car(logged_in_app, "Sauce Labs Bike Light")   
    catalog_page.add_to_car(logged_in_app, "Sauce Labs Bolt T-Shirt")      
    expect(catalog_page.cart_link).to_have_text("3") 
       
    catalog_page.cart_link.click()
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/cart.html")
        
    car_page = CarPage(logged_in_app)
    assert car_page.inventory_items_names.filter(has_text="Sauce Labs Backpack") is not None
    assert car_page.inventory_items_names.filter(has_text="Sauce Labs Bike Light") is not None
    assert car_page.inventory_items_names.filter(has_text="Sauce Labs Bolt T-Shirt") is not None
    
    car_page = CarPage(logged_in_app)  
    car_page.remove_product_from_car(logged_in_app, "Sauce Labs Backpack")
    car_page.remove_product_from_car(logged_in_app, "Sauce Labs Bike Light")
    car_page.remove_product_from_car(logged_in_app, "Sauce Labs Bolt T-Shirt")   
    
    
@pytest.mark.parametrize("product_name", [
    "Sauce Labs Backpack",
    "Sauce Labs Bolt T-Shirt"
])
def test_delete_product_from_car(logged_in_app: Page, product_name: str):
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, product_name)
    
    catalog_page.cart_link.click()
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/cart.html")
    
    car_page = CarPage(logged_in_app)  
    car_page.remove_product_from_car(logged_in_app, product_name)
    
    assert car_page.inventory_items_names.filter(has_text=product_name).count() == 0, f"No se encontró el producto '{product_name}'"
    
@pytest.mark.parametrize("product_name", [
    "Sauce Labs Bolt T-Shirt"
])
def test_update_car_link_after_delete_product(logged_in_app: Page, product_name: str):
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, product_name)
    expect(catalog_page.cart_link).to_have_text("1")
    
    catalog_page.cart_link.click()
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/cart.html")
    
    car_page = CarPage(logged_in_app)  
    car_page.remove_product_from_car(logged_in_app, product_name)
    
    catalog_page.navigate(catalog_page.url)
    expect(catalog_page.cart_link).to_have_text("")