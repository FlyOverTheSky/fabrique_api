# Тестовое задание для Fabrique
Тестовый сервис для создания рассылок и отправок сообщений на внешнее api.
Папки venv и env были оставлены намерено.
Docker-compose не доработан, поэтому пользоваться им не нужно

## Технологии
- Pytohn
- DRF
- Celery
- Redis

## Использование
Чтобы запустить проект понадобиться 4 терминала.
1) server
2) celery-worker
3) celery-beat
4) redis

По каждому терминалу 
Server:

```
python -m venv venv
```

```
sourve venv/Scripts/activate
```

```
pip install -r api/requirements.txt
```

```
python api/backend/manage.py migrate
```
```
python api/backend/manage.py runserver
```

Celery-worker
```
cd api/backend
```
```
celery -A backend worker -l info
```

Celery-beat
```
cd api/backend
```
```
celery -A backend beat -l info
```

Redis
терминал ubuntu
```
sudo apt install redis
```
```
redis-server
```
Проверка подключеня:
```
redis-cli
ping
```
