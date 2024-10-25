### Трекер давления
![project test](https://github.com/aeonva1ues/pressure_monitor/actions/workflows/django.yml/badge.svg)
___
#### Функционал

Для доступа к заметкам необходимо войти в аккаунт. 
```
Логин: user 
Пароль: 12345
```

Аккаунт заранее создан при помощи кастомной команды (tracker/management/commands/load_user.py).

После входа в аккаунт появляется доступ к просмотру своих записей давления, добавлении новых заметок, а также получение статистики.

Для добавления новой записи необходимо нажать на кнопку "Добавить запись", а затем заполнить форму в модальном окне.

На главной странице показывается последняя запись пользователя, а если указать промежуток времени и нажать "Показать" то будут отображены все записи за данный промежуток времени, а также средние значения систолического и диаболического давления

**Стек: django 3.2 , postgres, bootstrap**

**Фичи:** кастомная команда для быстрого создния пользователя, менеджер модели, покрытие тестами, CI/CD с линтером и запуском джанго-тестов, запуск через докер, оптимизированные запросы в бд (select_related), валидаторы у поля в модели, разделение шаблонов, разделение зависимостей проекта, переменные окружения


___
#### Установка
**1.1 Склонируйте репозиторий**
```
git clone https://github.com/aeonva1ues/pressure_monitor.git
```

**1.2 Задайте переменные окружения в файле .env**
```
cp .env.example .env
```
___
#### Запуск
**2.1.1 При помощи docker-compose:**
```
docker-compose up --build -d && docker-compose logs -f
```
**Выключение:**
```
docker-compose down --remove-orphans
```
___

**2.1.2 Вручную:**
* Создайте виртуальное окружение

*Linux:*
```
python3 -m venv venv
source venv/bin/activate
```
*Windows:*
```
python -m venv venv
.\venv\Scripts\activate
```

* Установите prod-зависимости:

*Linux:*
```
pip3 install -r requirements/prod.txt
```
*Windows:*
```
pip install -r requirements/prod.txt
```

* Проведите миграции базы данных

*Linux:*
```
python3 manage.py migrate
```
*Windows:*
```
python manage.py migrate
```

* Создайте тестового пользователя

*Linux:*

```
python3 manage.py load_user
```

*Windows:*
```
python manage.py load_user
```

* Запустите сервер 

*Linux:*
```
python3 manage.py runserver
```

*Windows:*
```
python manage.py runserver
```

*Обратите внимание: при ручном запуске проекта необходимо самостоятельно позаботиться о подъеме базы данных.*

___

**Lets go!**
 http://127.0.0.1:8000/
