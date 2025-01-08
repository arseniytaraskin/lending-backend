# Базовый образ
FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y libpq-dev gcc

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . /app/

# Создание папки media/images и копирование изображений
RUN mkdir -p /app/media/images

# Копирование папки media в контейнер
COPY media/images /app/media/images/

# Выполнение команд миграции и сбора статики
RUN python manage.py collectstatic --noinput

# Команда запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
