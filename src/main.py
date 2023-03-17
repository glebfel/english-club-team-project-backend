import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import auth_router
from news.router import news_router
from shifts.router import shifts_router
from src.config import settings
from tasks.router import tasks_router
from user.router import user_router

app = FastAPI(title='Child Camp API', version='1.0.0')
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(news_router)
app.include_router(shifts_router)
app.include_router(tasks_router)

# разрешим CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)