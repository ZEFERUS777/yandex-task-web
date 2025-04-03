import requests


url = "http://127.0.0.1:5000/api/jobs"


response_1 = requests.get(f"{url}")
if response_1.status_code == 200:
    print("Запрос на получение всех пользователей выполнен успешно. TEST1")


response_2 = requests.get(f"{url}/3")
if response_2.status_code == 200 and response_2.json()["id"] == 3:
    print("Запрос выполнен корректно TEST2")
else:
    print("Неверный id иои запрос  ", response_2.status_code)
