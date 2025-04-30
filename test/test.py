import requests


url = "http://127.0.0.1:5000/api/api_key/"

rsp_jo = {
    "email": "laketti@mail.ru11"
}

rsp = requests.post(url+"reg_api", params=rsp_jo)
print(rsp.reason)