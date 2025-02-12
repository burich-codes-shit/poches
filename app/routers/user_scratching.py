import json
from datetime import date

from fastapi import APIRouter, Depends, status, Request, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from typing import Annotated
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, and_
from starlette.templating import _TemplateResponse

from app.backend.db_depends_2 import get_db
from app.models.scratch import User, Comment

from bot_directory.admin_bot import send

#  Привязка роутеров, шаблонов, хэширование пароля
router = APIRouter(prefix='/scratch', tags=['scratch'])
templates = Jinja2Templates(directory='templates')
#bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ph = PasswordHasher()

#  Для вывода html с формами ввода требуется создать две конечные точки для get и post запросов
#  Создание пользователя
@router.get("/create")
async def create_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("registration.html", {'request': request})


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(request: Request,
                      db: Annotated[AsyncSession, Depends(get_db)],
                      login=Form(),
                      password: str =Form(),
                      email=Form()) -> HTMLResponse:
    #  Проверка условий создания нвого пользователя
    print(type(password))
    all_users_logins = len(list(await db.scalars(select(User).where(User.login == login))))
    all_users_emails = len(list(await db.scalars(select(User).where(User.email == email))))
    if all_users_logins > 0:
        return templates.TemplateResponse("error.html", {'request': request,
                                                         'error_name': "Пользователь с таким логином уже существует"})
    if all_users_emails > 0:
        return templates.TemplateResponse("error.html", {'request': request,
                                                         'error_name': "Пользователь с электронной почтой уже существует"})
    else:
        await db.execute(insert(User).values(login=login,
                                       password=ph.hash(password),
                                       email=email))
        await db.commit()
        send(message=f'Пользователь {login} с почтой {email} зарегестрировался')
        return templates.TemplateResponse("main.html", {'request': request, 'status': 'status.HTTP_201_CREATED'})


#  Логин пользователя
@router.get('/login')
async def login(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(request: Request,
                db: Annotated[AsyncSession, Depends(get_db)],
                login=Form(),
                password=Form()) -> _TemplateResponse:
    #try:
        #  ТЕСТОВОЕ ПРОВЕРКА СОВПАДЕНИЕ ХЭШИРОВАННОГО ПАРОЛЯ И ПАРОЛЯ ПОЛЬЗОВАТЕЛЯ ----- HashTest
        user_password = password
        stored_hash = (await db.scalar(select(User).where(User.login == login))).password
        print(f'{stored_hash}+++++++++++++++++++++++++++++++++')
        #  поиск в базе данных пользователя в соответствии с данными из формы
        user_params = await db.scalar(select(User).where(and_(User.login == login, User.password == password)))

        print(f'{user_params}+++++++++++++++++++++++++++++++++')
        # внесение данных пользователя в сессию (куки)
        if ph.verify(stored_hash, user_password):
            request.session['login'] = login
            try:
                user_login = request.session.get('login')
            except:
                user_login = 'user_name'

            # Перезапись куки партнера при повторном логировании
            partner = await db.scalar(select(User).where(User.login == user_login))
            request.session['partner'] = partner.partner
            print(user_login)
            print(request.session.get('partner'))

            return templates.TemplateResponse("main.html",
                                              {'request': request, 'status': 'status.HTTP_201_CREATED', 'user': user_params,
                                               'user_login': user_login})
        elif not ph.verify(stored_hash, user_password):
            return templates.TemplateResponse("error.html",
                                              {'request': request, 'error_name': "Неправильный пароль"})
    #except:
    #    return templates.TemplateResponse("error.html",
    #                                      {'request': request, 'error_name': "Возникла ошибка, проверьте данные"})


    #  elif user_params.password != password:
    #     return templates.TemplateResponse("error.html", {'request': request, 'error_name': "Неправильный пароль"})


#  Написание фидбэка
@router.get('/feedback')
async def feedback(request: Request,
                   db: Annotated[AsyncSession, Depends(get_db)]) -> _TemplateResponse:
    #  проверка куки, обработка ошибки
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'

    if not user_login or user_login == 'user_name':
        return templates.TemplateResponse("error.html", {'request': request, 'error_name': "Вы не залогинены"})

    # Запрос на все записи БД и внесение нового комментария
    all_users = await db.scalars(select(Comment).where(Comment.test == True))
    list_of_comments = []
    for user in all_users:
        user_data = [user.user_login, user.comment, str(user.date_of_creation)[:-9]]
        list_of_comments.append(user_data)

    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'

    return templates.TemplateResponse('feedback.html', {'request': request, 'user_login': user_login,
                                                        'list_of_comments': list_of_comments})


@router.post('/feedback')
async def feedback(request: Request,
                   db: Annotated[AsyncSession, Depends(get_db)],
                   comment: str = Form()) -> _TemplateResponse:
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'
    login = request.session.get('login')
    date_of_creation = date.today()
    await db.execute(insert(Comment).values(user_login=login,
                                      comment=comment,
                                      date_of_creation=date_of_creation))
    await db.commit()
    all_users = await db.scalars(select(Comment).where(Comment.test == True))
    list_of_comments = []
    for user in all_users:
        user_data = [user.user_login, user.comment, str(user.date_of_creation)[:-9]]
        list_of_comments.append(user_data)
    return templates.TemplateResponse("feedback.html", {'request': request, 'user_login': user_login,
                                                        'list_of_comments': list_of_comments})


# Роут с запросом на страницу скрэтчи
@router.get('/scratchy')
async def scratchy(request: Request, db: Annotated[AsyncSession, Depends(get_db)]) -> _TemplateResponse:
    # Переменная отвечающая за необходимость показа уведомления о незаполненном поле партнера
    show_context_window_partner_input = False

    #  Куки файлы юзернейма
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'

    #  Проверка залогиненного пользователя и получение читаемых данных о пользователе
    if not user_login or user_login == 'user_name':
        return templates.TemplateResponse("error.html", {'request': request, 'error_name': "Вы не залогинены"})
    else:
        user_info = await db.scalar(select(User).where(User.login == user_login))
        user_info = [user_info.login, user_info.partner, user_info.scratch_time_user, user_info.scratch_time_partner]
        if user_info[1] == 'Partner':
            show_context_window_partner_input = True
    return templates.TemplateResponse("scratchy.html", {'request': request,
                                                        'user_login': user_login,
                                                        'user_info': user_info,
                                                        'show_context_window_partner_input': show_context_window_partner_input})


#  Функция перевода времени из JS в секунды
def time_from_db_to_minutes(time: str):
    time = time.split(':')
    counter = 0
    counter += int(time[0]) * 60 * 60
    counter += int(time[1]) * 60
    counter += int(time[2])
    return counter


@router.post('/scratchy')
async def scratchy(request: Request,
                   db: Annotated[AsyncSession, Depends(get_db)],
                   ):
    # Перезапись куки логина пользователя
    show_context_window_partner_input = False
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'

    #  Информация о сессии из фронтенда
    request_body = await request.body()
    user_data_from_js = json.loads(request_body.decode('utf-8'))

    #  Данные пользователя из БД и условие показа уведомления о невнесенном информации о партнере
    user_info = await db.scalar(select(User).where(User.login == user_login))
    user_info = [user_info.login, user_info.partner, user_info.scratch_time_user, user_info.scratch_time_partner]
    if user_info[1] is None:
        show_context_window_partner_input = True

    #  Запись в БД данных о сессии пользователя
    if user_data_from_js['partnerName'] == 'user':
        time_from_js_to_minutes_box = time_from_db_to_minutes(user_data_from_js['timer'])
        updated_time = user_info[2] + time_from_js_to_minutes_box
        await db.execute(update(User).where(User.login == user_login).values(scratch_time_user=updated_time))
        await db.commit()
        print(time_from_js_to_minutes_box)
        print(user_info[2])
        print('---ВРЕМЯ ИЗМЕНЕНО---')
    elif user_data_from_js['partnerName'] == 'partner':
        time_from_js_to_minutes_box = time_from_db_to_minutes(user_data_from_js['timer'])
        updated_time = user_info[3] + time_from_js_to_minutes_box
        await db.execute(update(User).where(User.login == user_login).values(scratch_time_partner=updated_time))
        await db.commit()
        print(time_from_js_to_minutes_box)
        print(user_info[3])
        print('---ВРЕМЯ ИЗМЕНЕНО---')

    return {'user_info': user_info,
            'show_context_window_partner_input': show_context_window_partner_input,
            }


#  Настройки
@router.get('/settings')
async def settings(request: Request) -> _TemplateResponse:
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'
    if not user_login or user_login == 'user_name':
        return templates.TemplateResponse("error.html", {'request': request, 'error_name': "Вы не залогинены"})
    return templates.TemplateResponse('settings.html', {'request': request})


#  Форма для внесения данных о партнере
@router.post('/settings')
async def settings(request: Request,
                   db: Annotated[AsyncSession, Depends(get_db)],
                   partners_name=Form(),
                   user_sex=Form(),
                   partner_sex=Form(),
                   ) -> _TemplateResponse:
    user_login = request.session.get('login')
    await db.execute(update(User).where(User.login == user_login).values(partner=partners_name,
                                                                   user_sex=user_sex,
                                                                   partner_sex=partner_sex))
    await db.commit()
    request.session['partner'] = partners_name
    return templates.TemplateResponse('settings.html', {'request': request})


#  Персональная и глобальная статистика пользователей
@router.get('/statistics')
async def statistics(request: Request,
                     db: Annotated[AsyncSession, Depends(get_db)]) -> HTMLResponse:
    try:
        user_login = request.session.get('login')
    except:
        user_login = 'user_name'

    if not user_login or user_login == 'user_name':
        return templates.TemplateResponse("error.html", {'request': request, 'error_name': "Вы не залогинены"})

    #  Запрос информации по пользователю
    user_info = await db.scalar(select(User).where(User.login == user_login))
    user_info = [user_info.login, user_info.partner, user_info.scratch_time_user, user_info.scratch_time_partner, user_info.user_sex, user_info.partner_sex]

    # Запрос всех пользователей
    all_users = await db.scalars(select(User).where(User.id > 0))
    total = 0
    user_time = 0
    partner_time = 0
    male_time = 0
    female_time = 0
    all_users_count = 0

    for user in all_users:
        total += (user.scratch_time_user + user.scratch_time_partner)
        user_time += user.scratch_time_user
        partner_time += user.scratch_time_partner
        all_users_count += 1
        if user.user_sex == 'Male':
            male_time += user.scratch_time_user
        elif user.user_sex == 'Female':
            female_time += user.scratch_time_user
        else:
            pass

        if user.partner_sex == 'Male':
            male_time += user.scratch_time_partner
        elif user.partner_sex == 'Female':
            female_time += user.scratch_time_partner
        else:
            pass


    return templates.TemplateResponse('statistics.html', {'request': request,
                                                          'user_info': user_info,
                                                          'total': total,
                                                          'user_time': user_time,
                                                          'partner_time': partner_time,
                                                          'all_users_count': all_users_count,
                                                          'male_time': male_time,
                                                          'female_time': female_time,
                                                          })


@router.post('/bugreport')
async def bugreport(request: Request, bugreport=Form()):
    print(f'report sent {bugreport}')
    send(message=f"❌Вам прислали новый баг, бегом исправлять:❌\n{bugreport}")
    return templates.TemplateResponse("main.html", {'request': request})

#  TEST FUNCTIONS _________________________________________________


@router.get('/test')
async def test(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    return templates.TemplateResponse("test.html", {'request': request})


@router.post('/test')
async def test(request: Request):
    request_body = await request.body()
    print(request_body.decode('utf-8'))

    template = templates.TemplateResponse("test.html", {"request": request})
    return {'1': '2'}
