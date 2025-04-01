from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage

def test_show_inventory(logged_in_app: Page):
    """
    Verifies that the inventory page shows 6 items.
    
    This test navigates to the inventory page and verifies that 6 items are visible.
    """
    
    catalog_page = CatalogPage(logged_in_app)  
    expect(catalog_page.inventory_item_name).to_have_count(6)
    
def test_productos_description(logged_in_app: Page):
    """
    Verifies that the inventory page shows 6 items with their descriptions and prices and
    that each item has an "Add to cart" button.
    
    This test navigates to the inventory page and verifies that 6 items are visible,
    each one with its description and price. It also verifies that each item has a button
    with the text "Add to cart".
    """
    catalog_page = CatalogPage(logged_in_app)
    expect(catalog_page.inventory_item_description).to_have_count(6)
    expect(catalog_page.inventory_item_price).to_have_count(6)
    product_list = catalog_page.inventory_item_description.all()
    for product in product_list:
        expect(product).to_contain_text("Add to cart")
        
def test_sorting_products_by_name_in_reverse_alphabetical_order(logged_in_app: Page):
    """
    Verifies that the products can be sorted by name in reverse alphabetical order.
    
    This test navigates to the inventory page, gets the initial list of products,
    sorts them by name in reverse alphabetical order, and verifies that the
    sorted list matches the initial list sorted in reverse alphabetical order.
    """
    catalog_page = CatalogPage(logged_in_app)
    initial_products = catalog_page.inventory_item_description.all()
    catalog_page.click_product_sort(logged_in_app, "za")
    sorted_products = catalog_page.inventory_item_description.all()
    assert catalog_page.get_list_products_name(initial_products) == sorted(
        catalog_page.get_list_products_name(sorted_products), reverse=True
    )
    
def test_sorting_products_by_price(logged_in_app: Page):
    """
    Verifies that the products can be sorted by price in ascending order.

    This test navigates to the inventory page, retrieves the initial list of product prices,
    sorts them by price in ascending order, and verifies that the sorted list matches the
    expected order.
    """
    catalog_page = CatalogPage(logged_in_app)
    precios_inicial_float = [float(price.replace("$", "")) for price in catalog_page.get_list_products_name(catalog_page.inventory_item_price.all())]
    catalog_page.click_product_sort(logged_in_app, "lohi")
    precios_final_float = [float(price.replace("$", "")) for price in catalog_page.get_list_products_name(catalog_page.inventory_item_price.all())]
    assert precios_final_float == sorted(precios_final_float)
  

    
    
    
  