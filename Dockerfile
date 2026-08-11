# Используем официальный образ Python
FROM python:3.9-slim-bullseye

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . /app
WORKDIR /app

# Запускаем сервер с правильным портом
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=${PORT}"]
