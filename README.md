Данный проект предоставляет API для управления текстовыми блоками и изображениями на лендинге. Он включает функции для добавления, редактирования, удаления и получения контента. А также интеграцию с AI для генерации уникального контента.

**Для запуска проекта необходимо**:
1. Python 3.9+ (рекомендуется)
2. Git
3. Virtualenv (для управления виртуальным окружением)
4. sqlite (или другой поддерживаемый БД)

**Установка:**
1. Клонируйте репозиторий
2. Создайте виртуальное окружение и активруйте его
```
python -m venv venv
source venv/bin/activate   # Для Linux/MacOS
venv\Scripts\activate      # Для Windows
```
3. Установите зависимости проекта
```
pip install -r requirements.txt
```
**Запуск проекта**
1. Примените миграции
```
python manage.py makemigrations
python manage.py migrate
```
2. Создайте суперпользователя
```
python manage.py createsuperuser
```
3. Запустите сервер
```
python manage.py runserver
```
python manage.py runserver
```

