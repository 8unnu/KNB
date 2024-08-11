import uvicorn
from fastapi import FastAPI
from api.endpoints import knb_router

app = FastAPI()
app.include_router(knb_router)

if __name__ == "__main__":
    uvicorn.run("main:app")