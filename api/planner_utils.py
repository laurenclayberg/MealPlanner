import random

class PlannerParams:

    def __init__(self):
        # Set meal planner defaults
        self.dinner_days = 7
        self.dinner_servings = [2,2,2,2,2,2,2]

def verify_parameters(planner_params):
    ''' Checks to make sure parameters do not conflict
    '''
    return True

def generate_meal_plan(recipes, planner_params):
    ''' Generate a meal plan

        This meal plan generator has support for the following parameters:
        - dinner_days (integer)
        - dinner_servings (list(integer))

        Returns: a list of formatted recipes
    '''
    # Choose recipes for the meal plan
    count_meal_plan_recipes = planner_params.dinner_days
    count_database_recipes = len(recipes)
    selection_range = max(count_meal_plan_recipes, count_database_recipes)

    recipe_selection = random.sample(range(selection_range), count_meal_plan_recipes)
    recipe_selection = [num % count_database_recipes for num in recipe_selection]

    # Convert recipes to correct servings per meal
    for i in range(len(recipes)):
        recipe = recipes[i]
        servings = planner_params.dinner_servings[i]
        multiplier = float(servings) / float(recipe['servings'])

        recipe['servings'] = multiplier * float(recipe['servings'])
        for ingredient in recipe['ingredients']:
            ingredient['quantity'] = multiplier * float(ingredient['quantity'])

    return [recipes[i] for i in recipe_selection]

def generate_grocery_list(recipes):
    ''' Create a grocery list from a list of recipes

        Returns: a list of nonrepeating ingredients and their quantities
            [{
                ingredient: <name>,
                quantity: <quantity>
            }, {...}]
    '''
    ingredients = {} # map of {<ingredient name>: [float, unit]}

    for recipe in recipes:
        recipe_ingredients = recipe['ingredients']
        for ingredient in recipe_ingredients:
            ingredient_name = ingredient['ingredient']
            ingredient_quantity = float(ingredient['quantity'])
            ingredient_unit = ingredient['unit']
            if ingredient_name not in ingredients:
                ingredients[ingredient_name] = [ingredient_quantity, ingredient_unit]
            else:
                ingredient_cur = ingredients[ingredient_name]
                if ingredient_cur[1] == ingredient_unit:
                    # units match, so just add quantities
                    ingredient_cur[0] += ingredient_quantity
                else:
                    # units do not match, so need to do a conversion
                    raise NotImplementedError

    return ingredients
