import time
import faker
import pytest
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage
from pages.car_page import CarPage
from pages.checkout_page import CheckOutPage

@pytest.mark.parametrize("product_name", [
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Backpack"
])
def test_complete_checkout(logged_in_app: Page, product_name):
    fake = faker.Faker()
    name = fake.first_name()
    last_name = fake.last_name()
    zip_code = fake.zipcode_in_state()
    
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, product_name) 
    product_price = catalog_page.get_product_price(logged_in_app, product_name)    
           
    catalog_page.cart_link.click()
    car_page = CarPage(logged_in_app)  
    car_page.checkout_button.click()    
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/checkout-step-one.html") 
    
    check_out_page = CheckOutPage(logged_in_app)
    check_out_page.fill_text(check_out_page.first_name_field, name)
    check_out_page.fill_text(check_out_page.last_name_field, last_name)
    check_out_page.fill_text(check_out_page.postal_code_field, zip_code)
    check_out_page.click_element(check_out_page.continue_button)
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/checkout-step-two.html") 
    expect(check_out_page.item_name).to_contain_text(product_name)
    assert product_price == check_out_page.get_product_price(logged_in_app, product_name)
    
    #--- Deleting product from car for maintain clean test ---
    catalog_page.cart_link.click()    
    car_page = CarPage(logged_in_app)  
    car_page.remove_product_from_car(logged_in_app, product_name)
    
@pytest.mark.parametrize("product_name", [
    "Sauce Labs Backpack"
])
def test_checkout_missing_data(logged_in_app: Page, product_name):
    fake = faker.Faker()
    name = fake.first_name()
    last_name = fake.last_name()
    zip_code = fake.zipcode_in_state()
    
    catalog_page = CatalogPage(logged_in_app)
    catalog_page.add_to_car(logged_in_app, product_name) 
    product_price = catalog_page.get_product_price(logged_in_app, product_name) 
    
    catalog_page.cart_link.click()
    car_page = CarPage(logged_in_app)  
    car_page.checkout_button.click()    
    expect(logged_in_app).to_have_url("https://www.saucedemo.com/checkout-step-one.html") 
    
    check_out_page = CheckOutPage(logged_in_app)
    check_out_page.fill_text(check_out_page.first_name_field, "")
    check_out_page.fill_text(check_out_page.last_name_field, last_name)
    check_out_page.fill_text(check_out_page.postal_code_field, zip_code)
    check_out_page.click_element(check_out_page.continue_button)
    expect(check_out_page.error_message).to_contain_text("Error: First Name is required")
    
    check_out_page.fill_text(check_out_page.first_name_field, name)
    check_out_page.fill_text(check_out_page.last_name_field, "")
    check_out_page.fill_text(check_out_page.postal_code_field, zip_code)
    check_out_page.click_element(check_out_page.continue_button)
    expect(check_out_page.error_message).to_contain_text("Error: Last Name is required") 
    
    check_out_page.fill_text(check_out_page.first_name_field, name)
    check_out_page.fill_text(check_out_page.last_name_field, last_name)
    check_out_page.fill_text(check_out_page.postal_code_field, "")
    check_out_page.click_element(check_out_page.continue_button)
    expect(check_out_page.error_message).to_contain_text("Error: Postal Code is required")     
    
