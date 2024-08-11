from .sqlite_db import (sql_operation, get_user_id,
                        get_games_results_wins, get_games_results_loses,
                        get_user_password, get_games_results)

from .knb import sign_converter, reverse_sign_converter

import random

async def get_completed_id(payload):
    id = await get_user_id(payload)
    completed_id = id[0][0]
    return completed_id

async def get_score(completed_id):
    wins = await get_games_results_wins(completed_id)
    loses = await get_games_results_loses(completed_id)
    score = f"{wins}:{loses}"
    return score

async def standart_index_context(payload, request):
    completed_id = await get_completed_id(payload)
    score = await get_score(completed_id)

    context = {
        "request": request,
        "score": score
    }

    return context

async def game_context(payload, sign, request):
    completed_id = await get_completed_id(payload)
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
    score = await get_score(completed_id)

    context = {
        'request': request,
        'result': f'{result}, you take {sign} ({sign2}) and ai take {ai_sign} ({ai_sign2})',
        'score': score
    }

    return context

async def standart_user_context(payload, request):
    completed_id = await get_completed_id(payload)
    score = await get_score(completed_id)

    context = {
        "request": request,
        "score": score
    }

    return context

async def get_reg_user_error(users, username, password):
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
    return error

async def get_login_error(users, username, password):
    if username and password:
        for user_data in users:
            if user_data[0] == username:
                user_password = await get_user_password(username)
                if user_password[0][0] == password:
                    error = ""
                    return error
        error = "Data is incorrect"
    else:
        error = "Fields are empty"
    return error

async def user_create(username, password, request):
    operation_for_sql = f'''INSERT INTO users(username, password) VALUES ('{username}', '{password}');'''
    await sql_operation(operation_for_sql)
    error = "User has been created"

    context = {
        'request': request,
        'error': error
    }

    return context

async def history_context(payload, request):
    completed_id = await get_completed_id(payload)

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

    return context