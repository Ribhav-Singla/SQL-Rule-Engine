from enum import Enum


class Schema(Enum):
    ECOMMERCE = "ecommerce"
    BANKING = "banking"
    SOCIAL = "social"
    INVENTORY = "inventory"
    ANALYTICS = "analytics"


class Category(Enum):
    LOGIC = "logic"
    PERFORMANCE = "performance"
    BEST_PRACTICE = "best_practice"
    READABILITY = "readability"