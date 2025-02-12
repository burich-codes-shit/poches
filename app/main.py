from app.routers import user_scratching
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from fastapi import Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from app.backend.db_depends_2 import get_db
from app.models.scratch import User, Comment
from typing import Annotated
"""
Backend: 
    Python
    Fastapi

Frontend:
    HTML
    CSS
    Jinja2
    Bootstrap
    
Database:
    SQLite3
    
ORM:
    SQLalchemy
"""

app = FastAPI()
app.include_router(user_scratching.router)
templates = Jinja2Templates(directory='templates')
app.add_middleware(SessionMiddleware, secret_key="7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=")
#  uvicorn app.main:app --reload

#  docker-compose build --no-cache
#  docker-compose up -d
#  docker-compose exec web alembic upgrade head
#  docker-compose exec db psql --username=postgres_user --dbname=postgres_database
#  \l

#  docker ps -a
#  docker logs <>

# роут главной страницы
@app.get("/")
async def gates(request: Request) -> HTMLResponse:
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'
    return templates.TemplateResponse('main.html', {'request': request, 'user_login': user_login})


# Тестовые роуты, не в проде
@app.get('/read_session')
async def get_session(request: Request):
    all_session = request.session.items()
    return all_session

#  TODO:
#   - написать тесты
#   - верификация почты с помощью отправки кода
#   - смена пароля
#   - кнопка донатов через юкассу
#   - докер и докер композ
#   - купить хостинг
#   - залить на сервер
#   LATER:
#   - настройки баллов для домашних дел
#   - загрузку фотографии профиля в настройках
#   ---------------------------------
#   DONE:
#   - дата и время формат
#   - баг при отправке пустого коммента
#   - сделать автопрокрутку карточек используемых технологий на главной странице
#   - исправить баг с записью куки при неправильном заполнении формы логина
#   - долбоеб, у тебя не работает авторизация и кто угодно блять может писать что угодно, будь лучше...
#       - (solution: исколючить навигацию по сайту при отсутствии куки)
#   - название и иконка сайта
#   - нарисовать прогресс бары на шаблоне scratchy
#   - заменить дефолтное значение 'None' на 'partner'
#   - в разделе настроек сделать добавление имени партнера
#   - написать функцию конвертации времени в минуты
#   - запись куки партнера в settings
#   - написать таймер с отправкой значений в бд
#   - придумать оформление для страницы почеса
#   - исправить ошибку с появлением None при незалогиненном пользователе
#   - написать js функцию по отправке на сервер выбора пользователя, значения таймера и запись всего в базу данных
#   - документация!
#   - добавить хэширование пароля
#   - список всех пользователей с их статистикой
#   - глобальная статистика
#   - Дабавить пол, форму заполнения пола, статистику по полу
#   - написать requirments.txt
#   - telebot:
#       - админка
#       - сообщение о новых пользователях
#       - добавить таблицу для багрепортов и организовать их вывод и удаление
#       - Исправить ошибку requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
