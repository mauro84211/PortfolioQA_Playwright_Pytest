#   base_page.py

from playwright.sync_api import Page, Locator
import logging
from typing import Tuple
from datetime import datetime
import os


class BasePage:
    def __init__(self, page: Page, url):
      
        self.page = page
        self.timeout = 50000  # default wait time
        self.logger = logging.getLogger(__name__)
        self.url = url
        
        
        

    # ------------------------- General Methods ------------------------- #
    
    def navigate(self, url: str):
        """Navigate to a given URL"""
        self.page.goto(url, timeout=self.timeout)
        self.logger.info(f"Navegando a: {url}")
    
    def get_current_url(self) -> str:
        """Get actual URL"""
        return self.page.url
    
    def refresh_page(self):
        """Refresh the current page"""
        self.page.reload()
        self.logger.info("Refreshed page")
    
    def go_back(self):
        """Go back to the previous page"""
        self.page.go_back()
    
    def go_forward(self):
        """Move forward to the next page"""
        self.page.go_forward()
    
    def wait_for_page_load(self):
        """Wait for the page to load"""
        self.page.wait_for_load_state("networkidle")
        
    # ------------------------- Elements Interactions ------------------------- #
    
    def click_element(self, selector: Locator):
        """Click on an element"""
        selector.click()
        self.logger.info(f"Element {selector} clicked")
        
    def fill_text(self, selector: Locator, text: str):
        selector.fill(text)
