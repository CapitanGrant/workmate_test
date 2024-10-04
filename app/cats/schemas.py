from pydantic import BaseModel, Field, ConfigDict


class CCat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    color: str = Field(..., min_length=1, max_length=70, description="Цвет котенка, от 1 до 70 символов")
    age: int = Field(..., ge=0, le=24, description="Возраст котенка количество полных месяцев")
    breed: str = Field(..., min_length=1, max_length=80, description="Порода котенка, от 1 до 80 символов")
    description: str = Field(..., min_length=1, max_length=250, description="Описание котенка, от 1 до 250 символов")


class CatUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    age: int = Field(None, ge=0, le=24, description="Возраст котенка количество полных месяцев")
    breed: str = Field(None, min_length=1, max_length=80, description="Порода котенка, от 1 до 80 символов")
    color: str = Field(None, min_length=1, max_length=70, description="Цвет котенка, от 1 до 70 символов")
    description: str = Field(None, min_length=1, max_length=250, description="Описание котенка, от 1 до 250 символов")