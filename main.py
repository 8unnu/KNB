import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse



import random

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
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')

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
