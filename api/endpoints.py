from fastapi import (APIRouter, Request, Form,
                     Cookie, Depends, status)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from core.security import create_jwt_token, decode_jwt_token
from core.dao import (game_context, get_reg_user_error, get_login_error,
                      user_create, history_context, standart_index_context)
from core.postgres_db import pg_get_all_usernames

knb_router = APIRouter(
    prefix='',
    tags=['knb']
)

templates = Jinja2Templates(directory='templates')

@knb_router.get('/')
async def index(request: Request,
                users: dict = Depends(pg_get_all_usernames),
                jwt_token=Cookie(default=None)):
    if jwt_token:
        payload = decode_jwt_token(jwt_token)
        for user_data in users:
            if user_data[0] == payload:
                context = await standart_index_context(payload, request)
                return templates.TemplateResponse('index.html', context=context)
    return RedirectResponse(request.url_for('user'))

@knb_router.post('/')
async def game(request: Request,
               sign: str = Form(default=None),
               operation: str = Form(default=None),
               users: dict = Depends(pg_get_all_usernames),
               jwt_token=Cookie(default=None)):
    if jwt_token:
        payload = decode_jwt_token(jwt_token)
        for user_data in users:
            if user_data[0] == payload:
                if operation == "logout":
                    response = RedirectResponse(request.url_for('user'), status_code=status.HTTP_303_SEE_OTHER)
                    response.delete_cookie("jwt_token")
                    return response
                elif operation == "history":
                    response = RedirectResponse(request.url_for('history'), status_code=status.HTTP_303_SEE_OTHER)
                    return response

                if sign:
                    context = await game_context(payload, sign, request)
                    return templates.TemplateResponse('index.html', context=context)

                context = await standart_index_context(payload, request)
                return templates.TemplateResponse('index.html', context=context)
    return RedirectResponse(request.url_for('user'))

@knb_router.get('/users')
async def user(request: Request):
    return templates.TemplateResponse('profile.html', context={'request': request})

@knb_router.post('/users')
async def create_login_user(request: Request,
                      users: dict = Depends(pg_get_all_usernames),
                      username: str = Form(default=None),
                      password: str = Form(default=None),
                      operation: str = Form()):
    if operation == "register":
        error = await get_reg_user_error(users, username, password)
        if error != "":
            return templates.TemplateResponse('profile.html', context={'request': request, 'error': error})
        context = await user_create(username, password, request)
        return templates.TemplateResponse('profile.html', context=context)

    elif operation == "login":
        error = await get_login_error(users, username, password)
        if error != "":
            return templates.TemplateResponse('profile.html', context={'request': request, 'error': error})
        token = create_jwt_token({"sub": username})
        response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="jwt_token", value=token)
        return response

    elif operation == "logout":
        response = templates.TemplateResponse('profile.html', context={'request': request, 'error': "Logout completed"})
        response.delete_cookie("jwt_token")
        return response

@knb_router.get('/history')
async def history(request: Request,
                  users: dict = Depends(pg_get_all_usernames),
                  jwt_token=Cookie(default=None)):
    if jwt_token:
        payload = decode_jwt_token(jwt_token)
        for user_data in users:
            if user_data[0] == payload:
                context = await history_context(payload, request)
                return templates.TemplateResponse('history.html', context=context)
    return RedirectResponse(request.url_for('user'))

@knb_router.post('/history')
async def history_back(request: Request,
                       operation: str = Form(default=None)):
    if operation == "back":
        return RedirectResponse(request.url_for('index'))