# conftest.py

from playwright.sync_api import sync_playwright, Page, expect
from pages.login_page import LoginPage
import pytest
import os
from config import dev, staging, prod

@pytest.fixture(scope="session")
def browser_page():
    """
    Fixture for a browser page.

    The fixture is session-scoped, meaning that it is created once per test session.
    It launches a new browser instance using the chromium browser type and creates a new page.
    The page is yielded to the test, and the browser instance is closed when the test is finished.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture(scope="function")
def logged_in_app(browser_page: Page, config):
    """
    Fixture that logs in a user and returns the browser page.

    The fixture is session-scoped, meaning that it is created once per test session.
    It uses the browser_page fixture to get a browser page and the user fixture to get the user credentials.
    It navigates to the login page, logs in the user, and waits for the page to redirect to the home page.
    The fixture yields the browser page.
    
    Params:
        browser_page (Page): The browser page.
        user (UserByRole): The user to log in.
    """    
    
    login_page = LoginPage(browser_page)
    login_page.navigate(login_page.url)
    login_page.login(config.USERNAME, config.PASSWORD)
    expect(browser_page).to_have_url("https://www.saucedemo.com/inventory.html")
    yield browser_page
    
    
    
@pytest.fixture(scope="session")
def config(env="dev"):
    if env == "dev":
        return dev
    elif env == "staging":
        return staging
    elif env == "prod":
        return prod
    else:
        raise ValueError(f"Unknown environment: {env}")
