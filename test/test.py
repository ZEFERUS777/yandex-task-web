import requests


url = "http://127.0.0.1:5000/api/jobs/"


# response_1 = requests.get(f"{url}")
# if response_1.status_code == 200:
#     print("Запрос на получение всех пользователей выполнен успешно. TEST1")


# response_2 = requests.get(f"{url}/3")
# if response_2.status_code == 200 and response_2.json()["id"] == 3:
#     print("Запрос выполнен корректно TEST2")
# else:
#     print("Неверный id иои запрос  ", response_2.reason)


# data_rps4 = {
#     "apikey": "qfkVcePI3pf4RYM3gvcdZw",
#     "job_id": 2,
#     "email": "pomagomeddobri@gmail.com11" 
# }
# rsp4 = requests.delete(url+"/delete", params=data_rps4)
# if rsp4.status_code == 200:
#     print("Успешное удаление пользователя. TEST4")
# else:
#     print("Ошибка удаления пользователя. TEST4 ", rsp4.status_code)
    


common_data = {
    "apikey": "O-GOwsHdmROCCVRoZgAI3g",
    "finish": False,
    "email": "poa@gmail.com"
}

requests_data = [
    {
        "job_title": "Исследование personal",
        "team_lead_id": 12,
        "work_size": 200,
        "collaborators": "1223"
    },
    {
        "job_title": "Разработка модуля AI",
        "team_lead_id": 15,
        "work_size": 150,
        "collaborators": "15,45,23"
    },
    {
        "job_title": "Тестирование системы",
        "team_lead_id": 18,
        "work_size": 80,
        "collaborators": "18,92",
        "finish": True  # Переопределяем значение по умолчанию
    },
    {
        "job_title": "Анализ данных",
        "team_lead_id": 22,
        "work_size": 300,
        "collaborators": "22,11,33,44"
    },
    {
        "job_title": "Обновление безопасности",
        "team_lead_id": 14,
        "work_size": 120,
        "collaborators": "14,87",
        "email": "another-email@example.com"  # Другой email
    },
    {
        "job_title": "Оптимизация кода",
        "team_lead_id": 9,
        "work_size": 95,
        "collaborators": "9,12,15"
    }
]

for i, data in enumerate(requests_data, 1):
    # Объединяем общие данные с конкретными
    request_params = {**common_data, **data}
    
    # Отправляем запрос
    response = requests.post(
        url + "/add",
        params=request_params  # Если нужно отправлять в теле, замените params на json или data
    )
    
    print(f"Response {i} ({data['job_title']}):")
    print(f"Status: {response.status_code}")
    print(f"Reason: {response.reason}\n")



# data = {
#     "apikey": "RWg7zE7HTpuZRV4dpE1T6w",
#     "job_title": "Исследование",
#     "team_lead_id": 1,
#     "work_size": 200,
#     "collaborators": "1223",
#     "finish": False,
#     "email": "pomagomeddobri@mail.ru"
# }

# rsp6 = requests.put(url+"/update", params=data)
# print(rsp6.status_code)