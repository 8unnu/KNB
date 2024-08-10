import uvicorn
import random

from fastapi import (FastAPI, Request, Form,
                     Cookie, Depends, status)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from db.sqlite_db import (sql_operation, get_all_usernames,
                          get_user_password, get_user_id,
                          get_games_results_wins, get_games_results_loses,
                          get_games_results)

from app.security import create_jwt_token, decode_jwt_token

from app.endpoints import index

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
async def index_redirecter():
    return {"message": "visit to /knb"}

# @app.get('/')
# async def index(request: Request,
#                 users: dict = Depends(get_all_usernames),
#                 jwt_token=Cookie(default=None)):
#     if jwt_token:
#         payload = decode_jwt_token(jwt_token)
#         for user_data in users:
#             if user_data[0] == payload:
#
#                 id = await get_user_id(payload)
#                 completed_id = id[0][0]
#
#                 wins = await get_games_results_wins(completed_id)
#                 loses = await get_games_results_loses(completed_id)
#                 score = f"{wins}:{loses}"
#
#                 context = {
#                     "request": request,
#                     "score": score
#                 }
#                 return templates.TemplateResponse('index.html', context=context)
#     return RedirectResponse(request.url_for('user'))

@app.post('/')
async def game(request: Request,
               sign: str = Form(default=None),
               operation: str = Form(default=None),
               users: dict = Depends(get_all_usernames),
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

                id = await get_user_id(payload)
                completed_id = id[0][0]

                wins = await get_games_results_wins(completed_id)
                loses = await get_games_results_loses(completed_id)
                score = f"{wins}:{loses}"

                if sign:
                    sign = await sign_converter(sign)

                    arr = ['stone', 'scissors', 'paper']
                    ai_sign = arr[random.randint(0, 2)]

                    if ai_sign == sign:
                        result = "Draw"
                        operation = f'''INSERT INTO game_data(win, user_id) VALUES (2, {completed_id});'''
                        await sql_operation(operation)
                    elif ((ai_sign == "stone" and sign == "paper")
                          or (ai_sign == "scissors" and sign == "stone")
                          or (ai_sign == "paper" and sign == "scissors")):
                        result = "You win"
                        operation = f'''INSERT INTO game_data(win, user_id) VALUES (1, {completed_id});'''
                        await sql_operation(operation)
                    else:
                        result = "You lose"
                        operation = f'''INSERT INTO game_data(win, user_id) VALUES (0, {completed_id});'''
                        await sql_operation(operation)

                    sign2 = sign
                    ai_sign2 = ai_sign
                    ai_sign = await reverse_sign_converter(ai_sign)
                    sign = await reverse_sign_converter(sign)

                    context = {
                        'request': request,
                        'result': f'{result}, you take {sign} ({sign2}) and ai take {ai_sign} ({ai_sign2})',
                        'score': score
                    }

                    return templates.TemplateResponse('index.html', context=context)

                context = {
                    'request': request,
                    'score': score
                }

                return templates.TemplateResponse('index.html', context=context)
    return RedirectResponse(request.url_for('user'))
@app.get('/users')
async def user(request: Request):
    context = {
        'request': request
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

        operation_for_sql = f'''INSERT INTO users(username, password) VALUES ('{username}', '{password}');'''
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

@app.get('/history')
async def history(request: Request,
                  users: dict = Depends(get_all_usernames),
                  jwt_token=Cookie(default=None)):
    if jwt_token:
        payload = decode_jwt_token(jwt_token)
        for user_data in users:
            if user_data[0] == payload:

                id = await get_user_id(payload)
                completed_id = id[0][0]

                games_results = await get_games_results(completed_id)
                arr_games_results = []

                len_results = len(games_results)

                for game_result in reversed(games_results):
                    if game_result[0] == 1:
                        result = f"{len_results} - Win"
                    elif game_result[0] == 0:
                        result = f"{len_results} - Lose "
                    else:
                        result = f"{len_results} - Draw"
                    arr_games_results.append(result)
                    len_results -= 1

                context = {
                    'request': request,
                    'games_results': arr_games_results
                }

                return templates.TemplateResponse('history.html', context=context)
    return RedirectResponse(request.url_for('user'))

@app.post('/history')
async def history_back(request: Request,
                       operation: str = Form(default=None)):
    if operation == "back":
        return RedirectResponse(request.url_for('index'))