import uvicorn as uvicorn
from fastapi import FastAPI

from src import auth, news, shifts
from src.config import settings

app = FastAPI(title='Child Camp API', version='1.0.0')
app.include_router(auth.router)
app.include_router(news.router)
app.include_router(shifts.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FAST_API_HOST, port=settings.FAST_API_PORT)