# Проект **yamdb_final**

## Коротко о проекте

Учебный проект по работе workflow на основе проекта api_yamdb.


## Как запустить проект:

1. Установить Docker и Docker-compose на свой сервер:
``` bash
sudo apt upgrade -y
sudo apt install docker.io
sudo apt-get -y install python-pip
sudo pip install docker-compose
chmod +x /usr/local/bin/docker-compose
```

2. Создать файл <в созданной ранее директории проекта> docker-compose.yaml и заполнить его :

``` python
version: '3.8'
services:
  db:
   image: postgres:13.0-alpine
  volumes:
    - /var/lib/postgresql/data/
  env_file:
    - ./.env
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    timeout: 10s
    interval: 1s
    retries: 10

  web:
    depends_on:
      db:
        condition: service_healthy
    image: danilovkzn/infra_sp2:ver.1.1.8
    restart: always
    env_file:
      - ./.env
  nginx:
    image: nginx:1.21.3-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_value:/var/html/static/
      - media_value:/var/html/media/
    depends_on:
      - web
volumes:
  static_value:
  media_value:
```
3.  В этой же директории создать папку nginx:
``` bash
sudo mkdir nginx/
cd nginx/
```
   В папке nginx создать файл конфигурации для nginx:
``` bash
sudo touch default.conf
```
И заполнить его:
``` python
server {
    listen 80;
    server_name <IP your server>;

    location /static/ {
        root /var/html/;
    }
    
    location /media/ {
        root /var/html/;
    }
    
    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://web:8000;
    }

    server_tokens off;
}
```
4.  Создать и заполнить файл .env в директории , где расположен docker-compose:
``` Python
SECRET_KEY = 'Ключ приложения'
DB_ENGINE = 'Используемая БД'
DB_NAME = 'Имя БД'
POSTGRES_USER = 'Имя пользователя'
POSTGRES_PASSWORD = 'Пароль'
DB_HOST = 'Название кониейнера в docker-compose'
DB_PORT = 'Порт для подключения к БД'
SER_YANDEX = 'IP сервера'
```

5. Собрать образы 
``` bash
sudo docker pull danilovkzn/infra_sp2:latest
sudo docker-compose up -d --build
```
6. Зайти в контейнер web:
``` bash
sudo docker exec -it <CONTAINER_ID> bash
```
7. Заполнить БД данными и создать пользователя:

``` bash
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

8. Технологии
```
Python
Docker
Docker-compose
Nginx
Postgres
Gunicorn
```
9. Автор
```
Данилов Николай
``` 

10. Ссылка на проект
```
http://51.250.99.229/api/v1/
```
![example workflow](https://github.com/DanilovKZN/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
