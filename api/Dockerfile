FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["fastapi", "run", "app.py", "--port", "5000"]