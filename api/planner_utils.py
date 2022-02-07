import random
import copy

'''
TODO
Generate meal plan
- Include specific recipe IDs to include
- Allow fish/red meat/vegetarian limits
- Allow include specific ingredients
- Disallow changing servies of certain recipes (ex. lasagna)
'''

class PlannerParams:

    def __init__(self):
        # Set meal planner defaults
        # TODO - set to real defaults when done with testing
        self.dinner_servings = [6,2,2,2,8] # list(integer)
        self.recipe_ids = ["fb19b4eb-6efd-453f-a8ea-2d21e682a7f3", None, None, None, None] # list(string)

def verify_parameters(planner_params):
    ''' Checks to make sure parameters do not conflict
    '''
    dinner_servings = planner_params.dinner_servings
    recipe_ids = planner_params.recipe_ids
    if dinner_servings and recipe_ids and len(dinner_servings) != len(recipe_ids):
        # If recipes are provided, meal counts need to match between recipes and servings
        return False
    elif recipe_ids and not dinner_servings:
        # For every recipe included, you need to include servings required
        return False
    return True

def generate_meal_plan(recipes, planner_params):
    ''' Generate a meal plan

        This meal plan generator has support for the following parameters:
        - dinner_servings (list(integer))

        Returns: a list of formatted recipes
    '''
    count_chosen_recipes = sum([int(x != None) for x in planner_params.recipe_ids])

    # Choose recipes for the meal plan
    count_meal_plan_recipes = len(planner_params.dinner_servings) - count_chosen_recipes
    count_database_recipes = len(recipes)
    selection_range = max(count_meal_plan_recipes, count_database_recipes)

    recipe_selection = random.sample(range(selection_range), count_meal_plan_recipes)
    recipe_selection = [num % count_database_recipes for num in recipe_selection]

    # Add in pre-chosen recipes
    other_recipes = [copy.deepcopy(recipes[i]) for i in recipe_selection]
    chosen_recipes = []
    idx = 0
    for recipe_id in planner_params.recipe_ids:
        if recipe_id != None:
            for recipe in recipes:
                if recipe_id == recipe['id']:
                    chosen_recipes.append(copy.deepcopy(recipe))
                    break
        else:
            chosen_recipes.append(other_recipes[idx])
            idx += 1

    # Convert recipes to correct servings per meal
    for i in range(len(chosen_recipes)):
        recipe = chosen_recipes[i]
        servings = planner_params.dinner_servings[i]
        multiplier = float(servings) / float(recipe['servings'])

        recipe['servings'] = multiplier * float(recipe['servings'])
        for ingredient in recipe['ingredients']:
            ingredient['quantity'] = multiplier * float(ingredient['quantity'])

    return chosen_recipes

def generate_grocery_list(recipes, ingredient_locations):
    ''' Create a grocery list from a list of recipes

        recipes: A list of recipes
        ingredient_locations: A map of ingredients to locations

        Returns: a list of nonrepeating ingredients sorted by store location
            [{
                location: <store location>
                items: [
                    {
                        ingredient: <name>,
                        quantity: <quantity>
                        unit: <unit>
                    }, {...}
                ]
            }, {...}]
    '''
    # Combine ingredients from the recipes
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

    # Generate the grocery list sorted by store location
    grocery_list = {}
    for ingredient in ingredients.keys():
        item_quantity = ingredients[ingredient][0]
        item_unit = ingredients[ingredient][1]
        item_entry = {'ingredient': ingredient, 'quantity': item_quantity, 'unit': item_unit}

        location = ingredient_locations[ingredient]
        if location == None:
            location = 'UNKNOWN'
        if location not in grocery_list:
            grocery_list[location] = [item_entry]
        else:
            grocery_list[location].append(item_entry)

    grocery_list = [{'location': k, 'items': v} for (k,v) in grocery_list.items()]

    return grocery_list
