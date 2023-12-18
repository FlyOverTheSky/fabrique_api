# Название проекта
Добавьте краткое описание проекта, опишите какую задачу он решает. 1-3 предложения будет достаточно. Добавьте бейджи для важных статусов проекта: статус разработки (в разработке, на поддержке и т.д.), статус билда, процент покрытия тестами и тд.


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
sudo apt install redis
redis-server

Проверка подключеня:
```
redis-cli
ping
```
