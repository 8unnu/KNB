import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints import knb_router

app = FastAPI()
app.include_router(knb_router)

app.mount('/static', StaticFiles(directory='static'))

if __name__ == "__main__":
    uvicorn.run("main:app")