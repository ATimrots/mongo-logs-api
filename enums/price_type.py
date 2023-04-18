from enum import Enum

class PriceType(str, Enum):
    BASE_PRICE = "base_price"
    COST_PRICE = "cost_price"
