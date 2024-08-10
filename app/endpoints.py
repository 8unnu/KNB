from fastapi import (APIRouter, Request, Form,
                     Cookie, Depends, status)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from db.sqlite_db import (sql_operation, get_all_usernames,
                          get_user_password, get_user_id,
                          get_games_results_wins, get_games_results_loses,
                          get_games_results)

from .security import decode_jwt_token

router = APIRouter(prefix='/knb', tags=['endpoints'])

templates = Jinja2Templates(directory='templates')
router.mount('/static', StaticFiles(directory='static'))

@router.get('/')
async def index(request: Request,
                users: dict = Depends(get_all_usernames),
                jwt_token=Cookie(default=None)):
    return {'message': 'hello world'}
    # if jwt_token:
    #     payload = decode_jwt_token(jwt_token)
    #     for user_data in users:
    #         if user_data[0] == payload:
    #             id = await get_user_id(payload)
    #             completed_id = id[0][0]
    #
    #             wins = await get_games_results_wins(completed_id)
    #             loses = await get_games_results_loses(completed_id)
    #             score = f"{wins}:{loses}"
    #
    #             context = {
    #                 "request": request,
    #                 "score": score
    #             }
    #             return templates.TemplateResponse('index.html', context=context)
    # return RedirectResponse(request.url_for('user'))