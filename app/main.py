import uvicorn
from fastapi import FastAPI
from app.cats.router import router as router_cats
from app.database import init_db
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w',
                    encoding='utf-8'  #  Указываем  кодировку  'utf-8'
                    )
logger = logging.getLogger(__name__)
app = FastAPI()
# Событие старта приложения
@app.on_event("startup")
async def on_startup():
    await init_db()  # Инициализация базы данных при старте

@app.get("/")
def home_page():
    return {"message": "Привет, это REST API для администратора онлайн выставки котят:!"}


app.include_router(router_cats)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost")