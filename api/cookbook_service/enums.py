from enum import Enum

class MealEnum(Enum):
    DINNER = "dinner"
    LUNCH = "lunch"
    BREAKFAST = "breakfast"
    SNACK = "snack"

class CuisineEnum(Enum):
    AMERICAN = "american"
    ITALIAN = "italian"
    MEXICAN = "mexican"
    INDIAN = "indian"

class IsleEnum(Enum):
    PRODUCE = "produce"
    DELI = "deli"
    MEAT = "meat"
    DAIRY = "dairy"
    BAKERY = "bakery"
    BAKING = "baking"
    INTERNATIONAL = "international"
    CONDIMENTS = "condiments"

class LabelEnum(Enum):
    INSTANT_POT = "instant_pot"
    GRILL = "grill"
