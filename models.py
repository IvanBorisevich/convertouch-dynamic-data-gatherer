import uuid
from typing import Optional
from pydantic import BaseModel, Field

class CurrencyRate(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    code: str = Field(...)
    coefficient: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "code": "USD",
                "coefficient": 1,
            }
        }


class CurrencyRateUpdate(BaseModel):
    code: Optional[str]
    coefficient: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "code": "USD",
                "coefficient": 1
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}