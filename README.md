# api_final

### Описание:

```
Учебный проект YaMDb посвящён работе с DjangoRESTAPi.
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
```

### Техническое описание проекта YaMDb:

```
В репозитории api_yamdb, помимо тестов, сейчас находится пустой Django-проект. По адресу http://127.0.0.1:8000/redoc/ к нему подключена документация будущего API. 
```

### Стек использованных технологий.:

```
 Python, Django RESTAPI, SQLite
```


### Установка:

```
Скачайте и установите Python 3.9
```

```
Клонируйте git clone 
```

```
Cоздать и активировать виртуальное окружение:
```

###  Команда для Windows.

```
python -m venv venv
```

###  Команда для Windows с указанием версии Python.
```
py -3.9 -m venv venv
```
###  Команда для Linux и macOS.

```
python3 -m venv venv
```
```
source venv/Scripts/activate
```
###  Команда для Linux и macOS с указанием версии Python.

```
python3.9 -m venv venv
```
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
Cкрипт наполнения БД:
```
python3 manage.py addcsv
```

# Пример запроса:

GET


/api/v1/titles/
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [],
"category": {}
}
]
}
```

POST

/api/v1/titles/

```
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```


