# Используем базовый образ Python
FROM python:3.12

# Устанавливаем переменные окружения для Python (для логирования и вывода в консоль)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию контейнера
WORKDIR /app

# Устанавливаем зависимости из requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app/
EXPOSE 8000