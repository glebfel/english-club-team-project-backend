import uvicorn as uvicorn
from fastapi import FastAPI

from auth.router import auth_router
from news.router import news_router
from shifts.router import shifts_router
from src.config import settings
from user.router import user_router

app = FastAPI(title='Child Camp API', version='1.0.0')
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(news_router)
app.include_router(shifts_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)