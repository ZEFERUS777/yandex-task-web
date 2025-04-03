# Документация по параметрам API 

Запрос для добавления работы по адресу ***http:/localhost:5000/api/jobs/add***\
Параметр | Значение
-------- | --------
**apikey** | Обязательный параметр, ключ доступа **type String**
**job_title** | Название работы, обязательный параметр **type String**
**team_lead_id** | ID капитана(начальника корпуса), обязательный параметр **type Integer**
**work_size** | Размер работы, обязательный параметр **type Integer**
**collaborators** | Коллеги по работе, обязательный параметр **type String**
**finish** | Окончена ли работа **type Boolean**
**email** | Email пользователя, обязательный параметр **type String**


## Пример запроса: 
```python 
url = "http://127.0.0.1:5000/api/jobs/add"  # убедитесь, что URL корректен
data = {
    "apikey": "uCMj0DM09PUm_H0Sw1Xh3Q",
    "job_title": "Исследование космоса",
    "team_lead_id": 1,
    "work_size": 200,
    "collaborators": "1223",
    "finish": False,
    "email": "magomed@mail.ru"
}


# Для тела запроса (рекомендуется для POST):
rsp = requests.post(url, params=data)
print(rsp.status_code)


rsp_2 = requests.post(f"{url}?apikey=uCMj0DM09PUm_H0Sw1Xh3Q&job_title=Asist&team_lead_id=12&work_size=200&collaborators=123&finish=True&email=magomed@mail.ru")
print(rsp_2.json())
```