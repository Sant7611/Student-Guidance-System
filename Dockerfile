FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9009

CMD ["daphne", "-b", "0.0.0.0", "-p", "9009", "student_guidance_system.asgi:application"]