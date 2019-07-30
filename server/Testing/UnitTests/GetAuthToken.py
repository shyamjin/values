import requests
import json
from settings import unittest_test_url

json_data= None
def getToken():
    url = unittest_test_url+"user/auth"
    payload = '{"user":"superadmin","password":"12345"}'
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    json_data = json.loads(response.text)
    return(str(json_data.get("data").get("Token")))