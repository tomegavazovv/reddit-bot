import time

def get_username_locator(page):
    return page.locator("input[name='username']")

def get_password_locator(page):
    return page.locator("input[name='password']")

def get_email_field_locator(page):
    return page.locator("input[name='email']")

def get_login_locator(page):
    return page.get_by_role("button", name="Log In")

def get_chat_btn_locator(page):
    return page.get_by_role("button", name="Open chat")

def get_rooms_with_notification_locator(page):
    page.wait_for_selector('rs-rooms-nav-room')    
    time.sleep(6)
    return page.query_selector_all('a.has-notifications')

def get_profile_chat_locator(page):
    return page.get_by_label("Open chat")

def get_message_input_locator(page):
    return page.get_by_placeholder("Message")

def get_message_send_btn_locator(page):
    return page.get_by_label("Send message")

def get_continue_btn_locator(page):
    page.wait_for_selector('button.continue')
    return page.query_selector('button.continue')

def get_create_btn_locator(page):
    return page.query_selector('button.create')

def get_recaptcha_box_locator(page):
    recaptcha_div = page.query_selector('div.recaptcha')
    height = recaptcha_div.evaluate("element => element.clientHeight")

    return recaptcha_div if height > 0 else None

def get_skip_btn_locator(page):
    return page.locator("button:has-text('Skip')")

def get_topic_btn_locator(page):
    return page.get_by_role("checkbox", name="Europe", exact=True)

def get_final_continue_btn_locator(page):
    return page.get_by_role("button", name="Continue")

def get_copy_btn_locator(page):
    return page.locator("button").filter(has_text="Copy").nth(1)