from fastapi import APIRouter, Depends
import logging

from app.cats.dao import CatsDAO
from app.cats.rb import RBCat
from app.cats.schemas import CCat, CatUpdate

# Настройка логгирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/cats', tags=['Работа с котятами'])


@router.get('/', summary='Получить всех котят')
async def get_all_cats(request_body: RBCat = Depends()) -> list[CCat]:
    logger.info(f"Получен запрос на получение всех котят с фильтрами: {request_body.to_dict()}")
    return await CatsDAO.find_all(**request_body.to_dict())


@router.get('/breeds_all', summary='Получить все породы')
async def get_all_breeds(request_body: RBCat = Depends()) -> list[str]:
    logger.info(f"Получен запрос на получение всех пород {request_body.to_dict()}")
    return await CatsDAO.find_all_breed()


@router.get('/by_filter', summary='Получить одного котенка по фильтру')
async def get_cat_by_filter(request_body: RBCat = Depends()) -> CCat | dict:
    logger.info(f"Получен запрос на получение котенка по фильтру: {request_body.to_dict()}")
    rez = await CatsDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        logger.warning(f"Котик с указанными вами параметрами не найден!")
        return {'message': f'Котик с указанными вами параметрами не найден!'}
    return rez


@router.get('/{id}', summary='Получить одного котенка по id')
async def get_cats_by_id(cats_id: int) -> CCat | dict:
    logger.info(f"Получен запрос на получение котенка с ID: {cats_id}")
    rez = await CatsDAO.find_one_or_none_by_id(cats_id)
    if rez is None:
        logger.warning(f"Котенок с ID {cats_id} не найден!")
        return {'message': f'Котенок с ID {cats_id} не найден!'}
    return rez


@router.post('/add/', summary='Добавить котенка в базу данных')
async def register_cat(cat: CCat) -> dict:
    logger.info(f"Получен запрос на добавление котенка в базу данных")
    check = await CatsDAO.add(**cat.dict())
    if check:
        return {'message': f'Котик успешно добавлен!, "cat": {cat}'}
    else:
        return {'message': f'Ошибка при добавлении котика'}


@router.put('/update_description/', summary='Обновление информации о котиках')
async def update_description(cat: CatUpdate) -> dict:
    check = await CatsDAO.update(filter_by={'id': cat.id}, age=cat.age, description=cat.description)
    if check:
        return {'message': f'Информация о котике успешно обновлена!'}
    else:
        return {'message': f'Ошибка при обновлении инофрмации о котике!'}


@router.delete('/delete/{cats_id}', summary='Удаление котика из базы данных')
async def delete_cat(cat: CCat) -> dict:
    check = await CatsDAO.delete(id=cat.id)
    if check:
        return {'message': f'Котик удален из базы данных!'}
    else:
        return {'message': 'Ошибка не получилось удалить котика из базы данных!'}
