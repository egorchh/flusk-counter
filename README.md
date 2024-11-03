# Отчет о развертывании приложения-счетчика на Flask с использованием PostgreSQL и Docker Compose

## Шаги по развертыванию:

### 1. Создание структуры проекта

Создана структура проекта с следующими файлами:

- `app.py`: Основной файл приложения на Flask.
- `docker-compose.yml`: Файл конфигурации Docker Compose для развертывания приложения и базы данных.
- `Dockerfile`: Файл для сборки Docker-образа приложения.
- `requirements.txt`: Список зависимостей Python для проекта.

### 2. Установка необходимых зависимостей

В `requirements.txt` были добавлены следующие зависимости:

```plaintext
flask
redis
flask-sqlalchemy
psycopg2-binary
```

### 3. Настройка PostgreSQL в Docker Compose

В файле `docker-compose.yml` была добавлена конфигурация для сервиса PostgreSQL:

```yml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5001:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
      DATABASE_URL: postgres://postgres:postgres@db:5432/postgres
  db:
    image: "postgres:alpine"
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### 4. Создание приложения на Flask

В файле `app.py` была реализована основная логика приложения. Для работы с базой данных PostgreSQL была использована библиотека SQLAlchemy. Ниже приведен полный код приложения:

```python
import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

def log_request():
    client_info = request.headers.get('User-Agent')
    new_counter = Counter(client_info=client_info)
    db.session.add(new_counter)
    db.session.commit()

@app.route('/')
def hello():
    log_request()
    count = Counter.query.count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

### 5. Создание Dockerfile

В `Dockerfile` была указана информация для сборки Docker-образа приложения:

```dockerfile
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

### 6. Запуск приложения

```bash
docker-compose up --build
```

### 7. Проверка записей в PostgreSQL

Для проверки записей в базе данных использованы следующие шаги:

1. Подключение к контейнеру с PostgreSQL:

```bash
docker-compose exec db sh
```

2. Запуск `psql` для работы с базой данных:

```bash
psql -U postgres
```

3. Просмотр таблиц и записей:

Для просмотра списка таблиц выполнил:

```sql
\dt
```

Запрошены записи:

```sql
SELECT * FROM counter;
```