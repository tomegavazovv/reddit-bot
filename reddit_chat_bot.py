import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError
from my_selectors import *

load_dotenv()

class ChatBot:
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
            self.browser = self.playwright.chromium.launch(headless=False, executable_path=self.chromium_path)
            self.context = self.browser.new_context()
        if self.page is None:
            self.page = self.context.new_page()

    def login(self):
        self.page.goto("https://www.reddit.com/login")
        username_locator = get_username_locator(self.page); 
        password_locator = get_password_locator(self.page)
        login_button = get_login_locator(self.page)

        try:
            username_locator.fill(os.getenv('reddit_username'))
            password_locator.fill(os.getenv('reddit_password'))
            login_button.click()
        except TimeoutError as e:
            print(f"Error during login: {e}")
            self.close_browser()
            raise

    def check_notifications(self):
        try:
            chat_locator = get_chat_btn_locator(self.page)
            chat_locator.wait_for(state='attached')
            time.sleep(2)
            chat_locator.click()
            rooms_with_notification = get_rooms_with_notification_locator(self.page)
            return len(rooms_with_notification)
        except TimeoutError as e:
            print(f"Error checking notifications: {e}")
            return 0

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    def check_for_new_messages(self):
        self.launch_browser()
        try:
            self.login()
            num_notifications = self.check_notifications()
            print(f"Number of new notifications: {num_notifications}")
        finally:
            self.close_browser()
            
    def open_user_chat(self, username):
        new_page = self.context.new_page()
        new_page.goto(f"https://www.reddit.com/user/{username}")
        open_chat_locator = get_profile_chat_locator(new_page)
        open_chat_locator.wait_for(state='attached')
        with self.context.expect_page() as page_info:
            open_chat_locator.click()
    
        chat_page = page_info.value
        return chat_page

    def send_message(self, page, message):
        message_input_locator = get_message_input_locator(page)
        message_input_locator.wait_for(state='attached')
        message_input_locator.fill(message)

        time.sleep(1)
        
        send_btn = get_message_send_btn_locator(page)
        time.sleep(2)
        send_btn.click()

    def send_message_to_user(self, username, message):
        self.launch_browser()
        try:
            self.login()
            time.sleep(5)
            chat_page = self.open_user_chat(username)
            self.send_message(chat_page, message)
            chat_page.close()
        finally:
            self.close_browser()
    
    def post(self):
        self.launch_browser()
        
    
if __name__ == "__main__":
    chromium_path = os.getenv('CHROMIUM_PATH', '/Users/tomegavazov/Library/Caches/ms-playwright/chromium-1129/chrome-mac/Chromium.app/Contents/MacOS/Chromium')
    bot = ChatBot(chromium_path)
    bot.send_message_to_user('Squancher70', "mamati deeba")
