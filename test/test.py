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


data_rps4 = {
    "apikey": "uCMj0DM09PUm_H0Sw1Xh3Q",
    "job_id": 3,
    "email": "magomed@mail.ru" 
}
rsp4 = requests.delete(url+"/delete", params=data_rps4)
if rsp4.status_code == 200:
    print("Успешное удаление пользователя. TEST4")
else:
    print("Ошибка удаления пользователя. TEST4 ", rsp4.status_code)