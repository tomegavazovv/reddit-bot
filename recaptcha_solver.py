import re
import time
import requests

def get_recaptcha_cookie(html_content):

  client = requests.Session()
  CAPSOLVER_API_KEY = "CAP-3FFFAF73B730D83FD7A85CDE280EB2E4"
  CAPSOLVER_API_ENDPOINT = "https://api.capsolver.com/createTask"

  WEBSITE_URL = "https://reddit.com/register"  

  data = {
      "clientKey": CAPSOLVER_API_KEY,
      "task": {
          "type": "ReCaptchaV2Task",
          "websiteURL": WEBSITE_URL,
          "websiteKey": '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC',
          "isInvisible": False,
      }
  }


  task_id_response = client.post(CAPSOLVER_API_ENDPOINT, json=data)
  task_id = task_id_response.json()['taskId']

  print(task_id)

  time.sleep(60)
  
  cookie_response = client.post("https://api.capsolver.com/getTaskResult", json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id}).json()
  print(cookie_response)
  if cookie_response["status"] == "ready":
    res = cookie_response["solution"]["gRecaptchaResponse"]
    
    return res
    
  else:
    print('failed')
    return None
  
  
  