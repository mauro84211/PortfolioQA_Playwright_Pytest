
from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        """
        Initialize the LoginPage class.

        Params:
            page (Page): The Playwright Page object.
        """
        super().__init__(page, "https://www.saucedemo.com" )
        self.username_field = page.locator("#user-name")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')

    def type_username(self, username):
        """
        Types the given username into the username field.

        Params:
            username (str): The username to enter.
        """
        self.username_field.fill(username)

    def type_password(self, password):
        """
        Types the given password into the password field.

        Params:
            password (str): The password to enter.
        """
        self.password_field.fill(password)

    def click_login_button(self):
        """Clicks the login button to submit the login form."""
        self.login_button.click()

    def login(self, username: str, password: str):
        """
        Logs in a user by filling in the username and password fields and clicking the login button.

        Params:
            username (str): The username to enter.
            password (str): The password to enter.
        """
        self.type_username(username)
        self.type_password(password)
        self.click_login_button()