from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage


    
def test_login_valid(browser_page: Page, config ):
    """
    Verifies that a valid login redirects to the inventory page.
    
    This test logs in with a valid username and password and verifies that the
    page redirects to the inventory page.
    """
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login(config.USERNAME, config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/inventory.html")
    
def test_login_invalid_user(browser_page: Page, config ):
    """
    Verifies that an invalid username does not log in.
    
    This test logs in with an invalid username and verifies that the
    page does not redirect to the inventory page and that the error
    message is visible.
    """
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login("invalid_user", config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/")
    assert login_page.error_message.is_visible()   
    expect(login_page.error_message).to_contain_text("Epic sadface: Username and password do not match any user in this service")
    
    
def test_login_empty_user(browser_page: Page ):
    """
    Verifies that an empty username does not log in.
    
    This test logs in with an empty username and verifies that the
    page does not redirect to the inventory page and that the error
    message is visible.
    """
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.username_field.fill("")
    login_page.password_field.fill("")
    login_page.login_button.click()
    expect(browser_page).to_have_url("https://www.saucedemo.com/")
    assert login_page.error_message.is_visible()
    expect(login_page.error_message).to_contain_text("Epic sadface: Username is required")
    
def test_close_session(browser_page: Page, config):
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login(config.USERNAME, config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/inventory.html")
    
    catalog_page = CatalogPage(browser_page)    
    expect(catalog_page.hamburger_menu).to_be_visible()
    login_page.click_element(catalog_page.hamburger_menu)
    
    expect(catalog_page.logout_button).to_be_visible()
    login_page.click_element(catalog_page.logout_button)
    expect(browser_page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.username_field).to_be_visible()
    expect(login_page.password_field).to_be_visible()
    
def test_blocked_user(browser_page: Page, config):
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login(config.LOCKED_USER, config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")
    
def test_performance_glitch_user(browser_page: Page, config):
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login(config.GLITCH_USER, config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/inventory.html")
    
    catalog_page = CatalogPage(browser_page)
    expect(catalog_page.inventory_item_description).to_have_count(6)
    expect(catalog_page.inventory_item_price).to_have_count(6)