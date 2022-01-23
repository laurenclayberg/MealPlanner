# Data

At some point I plan on storing the recipes in an actual database, but for now all of the recipe and ingredient records will live here.

## Recipe Schema
```json
{ 
  "id": "example id",
  "name": "example name",
  "credit": "example credit",
  "time": 30,
  "servings": 2,
  "rating": 4,
  "meal_categories": [ "category 1", "category 2" ],
  "cuisine_categories": [ "category 3" ],
  "custom_categories": [ "category 4" ],
  "instructions": [ "instruction 1", "instruction 2" ],
  "advance_prep": [ "prep 1" ],
  "advance_prep_max_days": 3,
  "ingredients": {
    "ingredient 1 id": [ 8, "oz" ],
    "ingredient 2 id": [ 1.5, "cup"]
  },
  "substitutes": {
    "ingredient 1": [ "alternative 1", "alternative 2" ],
    "ingredient 2": [ "alternative 3" ]
  }
}
```
Time is designated in minutes. Rating is a score 1 to 5 with 5 being the best.
## Ingredient Schema
```json
{ 
  "id": "example id",
  "name": "example name",
  "store_measurement": "can",
  "store_conversion":[ 16.0, "oz" ],
  "quantity": 1,
  "location": "produce"
}
```
The ingredient object represents one item you would purchase in the store. For example, a recipe might ask for 3 tablespoons of tomato paste, but it can only be bought as an 8 oz can. The store conversion is the simplest conversion to a standard measurement. 
