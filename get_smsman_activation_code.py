import requests
import os 
import time

def get_sms_activation_code(request_id):
    token = os.getenv('smsman_api_key')

    
    res = requests.get(f"https://api.sms-man.com/control/get-sms?token={token}&request_id={request_id}")
    
    time.sleep(40)
    
    res = requests.get(f"https://api.sms-man.com/control/get-sms?token={token}&request_id={request_id}")
    data = res.json()
    
    if data['sms_code']:
        return data['sms_code']
    
    time.sleep(30)
    res = requests.get(f"https://api.sms-man.com/control/get-sms?token={token}&request_id={request_id}")
    data = res.json()
    
    if data['sms_code']:
        return data['sms_code']
    
    return None
        
        