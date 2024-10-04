import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.cats.router import router


app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_get_all_cats():
    """
    Тест на получение всех котиков.

    Этот тест проверяет маршрут получения всех котиков.
    Ожидается, что ответом будет список (даже если он пустой) и код статуса 200.
    """
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.get("/cats/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Проверяем, что ответ - это список


@pytest.mark.asyncio
async def test_get_all_breeds():
    """
    Тест на получение всех пород котиков.

    Этот тест проверяет маршрут, который возвращает список всех пород котиков.
    Ожидается, что ответом будет список и код статуса 200.
    """
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.get("/cats/breeds_all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_cat_by_filter():
    """
    Тест на получение котика по фильтру.

    Этот тест проверяет маршрут получения котика по параметрам фильтра (например, возраст).
    Ожидается, что ответ будет либо сообщением об отсутствии котика, либо объектом котика.
    """
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.get("/cats/by_filter", params={"age": 2})
    assert response.status_code == 200
    assert "message" in response.json() or isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_get_cat_by_id():
    """
    Тест на получение котика по его ID.

    Этот тест проверяет маршрут получения конкретного котика по его ID.
    Ожидается, что ответом будет объект котика или сообщение, если котик не найден.
    """
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.get("/cats/{id}?cats_id=1")
    assert response.status_code == 200
    json_resp = response.json()
    assert "message" in json_resp or isinstance(json_resp, dict)


@pytest.mark.asyncio
async def test_add_cat():
    """
    Тест на добавление котика.

    Этот тест проверяет маршрут добавления нового котика в базу данных.
    Ожидается, что ответом будет сообщение об успешном добавлении котика и код статуса 200.
    """
    new_cat = {
        "id": 1,
        "color": "Черный",
        "age": 3,
        "breed": "Сиамский",
        "description": "Черный гладкошерстный."
    }
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.post("/cats/add/", json=new_cat)
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_update_cat():
    """
    Тест на обновление данных о коте.

    Этот тест проверяет маршрут обновления данных котика (например, возраста или описания).
    Ожидается, что ответом будет сообщение об успешном обновлении и код статуса 200.
    """
    updated_cat = {
        "id": 95,
        "age": 4,
        "description": "Обновленное описание."
    }
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.put("/cats/update_description/", json=updated_cat)
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_delete_cat():
    """
    Тест на удаление котика.

    Этот тест проверяет маршрут удаления котика из базы данных по его ID.
    Ожидается, что ответом будет сообщение об успешном удалении или ошибке, если котик не найден.
    """
    async with AsyncClient(app=app, base_url="http://cats") as ac:
        response = await ac.delete("/cats/delete/4")
        assert response.status_code == 200
