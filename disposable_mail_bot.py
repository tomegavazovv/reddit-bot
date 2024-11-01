import os
import time
from playwright_stealth import stealth_sync
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.my_selectors import *

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

    def create_account(self):
        self.launch_browser()
        try:
            self.page.goto("https://temp-mail.org/en/", wait_until='networkidle')
            copy_button = get_copy_btn_locator(self.page)
            self.page.wait_for_function("button => !button.disabled", copy_button)
            copy_button.click()
            
            print('huehue')
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
