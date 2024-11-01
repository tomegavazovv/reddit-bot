import requests
import os

def get_smsman_phone_number():
    token = os.getenv("smsman_api_key")
    country_id = 11  # Romania
    application_id = 136  # Yahoo

    res = requests.get(
        f"https://api.sms-man.com/control/get-number?token={token}&country_id={country_id}&application_id={application_id}"
    )

    data = res.json()
    request_id = data["request_id"]
    phone_number = data["number"]
    return {request_id: request_id, phone_number: phone_number}
