# Бронирование отелей
Это репозиторий учебного бэкенд проекта на FastAPI. В проекте учавствовали:
- SQLAlchemy + Alembic в качестве ORM.
- Celery для отложенных задач.
- Redis для кэширования и хранения задач celery.
- sqladmin для админки.
- logging в связке с sentry для логирования.
- pytest, docker


## Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn.
```
uvicorn app.main:app --reload
```  
### Celery & Flower
Для запуска Celery используется команда  
```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```
Для запуска Flower используется команда  
```
celery --app=app.tasks.celery:celery flower
``` 

### Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:  
```
docker build .
```  
Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

### Docker compose
Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды
```
docker compose build
docker compose up
```
