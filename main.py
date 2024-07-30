import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'))

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')

if __name__ == "__main__":
    uvicorn.run("main:app")