# Data

At some point I plan on storing the recipes in an actual database, but for now all of the recipe and ingredient records will live here.

## Recipe Schema
```json
{ 
  "id": "example id",
  "name": "example name",
  "source": "example source URL",
  "time": 30,
  "servings": 2,
  "rating": 4,
  "tags": [ "category 1", "category 2", "cuisine 1" ],
  "instructions": [ "instruction 1", "instruction 2" ],
  "ingredients": [
    {
        "ingredient": "salt",
        "quantity": 1,
        "unit": "tsp",
    },
    {
        "ingredient": "water",
        "quantity": 1.5,
        "unit": "cup",
    },
  ]
}

// Eventually:
{
  "advance_prep": [ "prep 1" ],
  "advance_prep_max_days": 3,
  "ingredients": [
    {
        "ingredient": "salt",
        "quantity": 1,
        "unit": "tsp",
        // Outer is "or", inner is "and"
        "alternates": [
            [
                {
                    "ingredient": "sugar",
                    "quantity": 1,
                    "unit": "tsp",
                }
            ]
        ]
    },
    {
        "ingredient": "water",
        "quantity": 1.5,
        "unit": "cup",
    },
  ]
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
