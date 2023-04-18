import sys
sys.path.append('/var/www/mongo-log-api/enums/')

from pydantic import BaseModel
from datetime import datetime
from price_type import PriceType
from project import Project
from typing import Union

class PriceChange(BaseModel):
    project: Project
    product_uuid: str
    price_type: PriceType
    old: Union[float, None] = None
    new: Union[float, None] = None
    time: datetime

    class Config:
        schema_extra = {
            "example": {
                "project": "project1",
                "product_uuid": "435089ef-297a-45ee-8327-81ef319116d1",
                "price_type": "cost_price",
                "old": 35.4,
                "new": 100.45,
                "time": "2023-04-11T15:53:00+05:00"
            }
        }
