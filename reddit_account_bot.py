import os
import time
from recaptcha_solver import *
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from my_selectors import *

load_dotenv()

class AccountBot:
    def __init__(self, chromium_path: str):
        self.chromium_path = chromium_path
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None

    def launch_browser(self):
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        if self.browser is None:
            self.browser = self.playwright.chromium.launch(
                headless=False, executable_path=self.chromium_path
            )
            self.context = self.browser.new_context()
        if self.page is None:
            self.page = self.context.new_page()

    def solve_recaptcha(self):
        recaptcha_box_locator = get_recaptcha_box_locator(self.page)
        if recaptcha_box_locator is not None:
            recaptcha_cookie = None
            while recaptcha_cookie is None:
                recaptcha_cookie = get_recaptcha_cookie(self.page.content())

            self.page.evaluate(f"document.getElementById('g-recaptcha-response').value='{recaptcha_cookie}'")
        
            time.sleep(3)

    def create_account(self):
        self.launch_browser()
        self.page.goto("https://www.reddit.com/register")
        email_locator = get_email_field_locator(self.page)
        continue_btn_locator = get_continue_btn_locator(self.page)
        password_locator = get_password_locator(self.page)
        try:
            email_locator.fill("tomegavaz@yahoo.com")
            continue_btn_locator.click()

            password_locator.wait_for()
            password_locator.fill("dekasibe223")
            
            self.solve_recaptcha()
            
            create_button_locator = get_create_btn_locator(self.page)
            create_button_locator.click()
            
            skip_button = get_skip_btn_locator(self.page)
            skip_button.click()
            
            topic_button = get_topic_btn_locator(self.page)
            topic_button.click()
            time.sleep(2)            
            continue_button = get_final_continue_btn_locator(self.page)
            continue_button.click()
            time.sleep(15)
        finally:
            self.close_browser()

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None


if __name__ == "__main__":
    chromium_path = os.getenv(
        "CHROMIUM_PATH",
        "/Users/tomegavazov/Library/Caches/ms-playwright/chromium-1129/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
    )
    bot = AccountBot(chromium_path)
    bot.create_account()
