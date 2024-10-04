from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True)
    color = mapped_column(String)
    age = mapped_column(Integer)
    breed = mapped_column(String)
    description = mapped_column(Text)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"breed={self.breed!r}, "
                f"color={self.color!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {"id": self.id, "color": self.color, "age": self.age, "breed": self.breed,
                "description": self.description}


async def get_table_info(engine):
    async with engine.begin() as conn:
        inspector = await conn.run_sync(inspect)
        if not inspector.has_table("cats"):
            await conn.run_sync(Base.metadata.create_all)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        try:
            # Проверка, есть ли записи в таблице
            result = await session.execute(text("SELECT COUNT(*) FROM cats"))
            count = result.scalar_one()
        except Exception as e:
            # Ловим исключение, если таблица еще не существует
            print(f"Ошибка при проверке таблицы: {e}")
            return
        # Если таблица пустая, добавляем записи
        if count == 0:
            cat1 = Cat(color="Черный", age=3, breed='Сиамский', description="Черный гладкошерстный.")
            cat2 = Cat(color="Рыжий", age=2, breed='Уличная', description="Рыжая голубоглазая.")

            session.add_all([cat1, cat2])
            await session.commit()
