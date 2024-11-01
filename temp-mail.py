import requests
import time
import hashlib


base_url = "https://privatix-temp-mail-v1.p.rapidapi.com"
headers = {
    "x-rapidapi-key": "5b20b496f7mshce71e57494d096ap165dcajsn322236f14071",
    "x-rapidapi-host": "privatix-temp-mail-v1.p.rapidapi.com"
}

def get_temp_email():
    url = f"{base_url}/request/domains/"
    response = requests.get(url, headers=headers)
    domains = response.json()
    
    if domains:
        username = "testuser123"
        email = f"{username}@{domains[0]}"
        return email
    return None

def get_emails(email):
    email_hash = hashlib.md5(email.encode()).hexdigest()
    
    url = f"{base_url}/request/mail/id/{email_hash}/"
    response = requests.get(url, headers=headers)
    return response.json()
