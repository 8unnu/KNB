import uvicorn
import random

from fastapi import (FastAPI, Request, Form,
                     Cookie, Depends, status)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from sqlite_db import sql_operation, get_all_usernames, get_user_password, get_user_token
from security import create_jwt_token, decode_jwt_token

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'))

if __name__ == "__main__":
    uvicorn.run("main:app")

async def sign_converter(sign):
    if sign == "✂️":
        return "scissors"
    elif sign == "🪨":
        return "stone"
    elif sign == "🧻":
        return "paper"

async def reverse_sign_converter(sign):
    if sign == "scissors":
        return "✂️"
    elif sign == "stone":
        return "🪨"
    elif sign == "paper":
        return "🧻"
@app.get('/')
async def index(request: Request,
                users: dict = Depends(get_all_usernames),
                jwt_token=Cookie(default=None)):
    if jwt_token:
        payload = decode_jwt_token(jwt_token)
        for user_data in users:
            if user_data[0] == payload:
                context = {
                    "request": request,
                    "score": "0:0"
                }
                return templates.TemplateResponse('index.html', context=context)
    return RedirectResponse(request.url_for('user'))

@app.post('/')
async def game(request: Request, sign: str = Form()):
    sign = await sign_converter(sign)

    arr = ['stone', 'scissors', 'paper']
    ai_sign = arr[random.randint(0, 2)]

    if ai_sign == sign:
        result = "Draw"
    elif ai_sign == "stone" and sign == "paper":
        result = "You win"
    elif ai_sign == "scissors" and sign == "stone":
        result = "You win"
    elif ai_sign == "paper" and sign == "scissors":
        result = "You win"
    else:
        result = "You lose"

    sign2 = sign
    ai_sign2 = ai_sign
    ai_sign = await reverse_sign_converter(ai_sign)
    sign = await reverse_sign_converter(sign)

    context = {
        'request': request,
        'result': f'{result}, you take {sign} ({sign2}) and ai take {ai_sign} ({ai_sign2})',
        'score': "0:0"
    }

    return templates.TemplateResponse('index.html', context=context)
@app.get('/users')
async def user(request: Request,
               users: dict = Depends(get_all_usernames)):
    context = {
        'request': request,
        'users': users
    }
    return templates.TemplateResponse('profile.html', context=context)

@app.post('/users')
async def create_user(request: Request,
                      users: dict = Depends(get_all_usernames),
                      username: str = Form(default=None),
                      password: str = Form(default=None),
                      operation: str = Form()):
    if operation == "register":
        error = ""
        if username and password:
            for user_data in users:
                if user_data[0] == username:
                    error = "This name is already taken"
                elif len(password) > 16:
                    error = "Password is too long"
                elif len(password) < 4:
                    error = "Password is too short"
        else:
            error = "Fields are empty"
        if error != "":
            context = {
                'request': request,
                'error': error
            }
            return templates.TemplateResponse('profile.html', context=context)

        operation_for_sql = f'''INSERT INTO users(username, password) VALUES ('{username}', '{password}')'''
        await sql_operation(operation_for_sql)
        error = "User has been created"
        context = {
            'request': request,
            'error': error
        }
        return templates.TemplateResponse('profile.html', context=context)

    elif operation == "login":
        error = ""
        if username and password:
            for user_data in users:
                if user_data[0] == username:
                    user_password = await get_user_password(username)
                    if user_password[0][0] == password:
                        token = create_jwt_token({"sub": username})
                        response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_303_SEE_OTHER)
                        response.set_cookie(key="jwt_token", value=token)
                        return response
            error = "Data is incorrect"
        else:
            error = "Fields are empty"
        if error != "":
            context = {
                'request': request,
                'error': error
            }
            return templates.TemplateResponse('profile.html', context=context)

    elif operation == "logout":
        error = "Logout completed"
        context = {
            'request': request,
            'error': error
        }
        response = templates.TemplateResponse('profile.html', context=context)
        response.delete_cookie("jwt_token")
        return response