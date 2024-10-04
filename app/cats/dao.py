from app.database import Cat
from app.dao.base import BaseDAO
class CatsDAO(BaseDAO):
    model = Cat

