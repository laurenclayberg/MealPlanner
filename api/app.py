from flask import Flask, request
import json
from .db import db

from .db_utils import *
from .recipe_utils import *
from .planner_utils import *

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to MealPlanner!'

@app.route('/ingredients', methods = ['POST', 'GET'])
def ingredients():
    if request.method == 'GET':
        # Search list of ingredients, potentially filtered by the query parameters
        # No query results in querying all ingredients
        query = request.args.get('q')
        raise NotImplementedError
    elif request.method == 'POST':
        raise NotImplementedError
    else:
        raise NotImplementedError

@app.route('/ingredient/<ingredient_id>', methods = ['GET', 'PUT', 'DELETE'])
def ingredient(ingredient_id):
    if request.method == 'GET':
        # Read an ingredient
        raise NotImplementedError
    elif request.method == 'PUT':
        # Update an ingredient
        raise NotImplementedError
    elif request.method == 'DELETE':
        # Delete an ingredient
        raise NotImplementedError
    else:
        raise NotImplementedError

@app.route('/recipes', methods = ['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        recipe = json.loads(request.data)
        # TODO: validate JSON using JSON schema
        conn = db()
        cur = conn.cursor()
        tag_ids = [touch_tag(app, cur, tag) for tag in sorted(set(recipe.get("tags", [])))]
        ingredient_to_id = {
            ing: touch_ingredient(app, cur, ing)
            for ing in sorted(set(
                ingredient_desc["ingredient"]
                for ingredient_desc in
                recipe.get("ingredients", [])
            ))
        }
        unit_to_id = {
            unit: touch_unit(app, cur, unit)
            for unit in sorted(set(
                ingredient_desc["unit"]
                for ingredient_desc in
                recipe.get("ingredients", [])
            ))
        }
        app.logger.debug("Tag ids: " + str(tag_ids))
        app.logger.debug("Ingredient to ID: " + str(ingredient_to_id))

        cur.execute("""
            INSERT INTO recipes (name, time, servings, instructions, source, rating)
            VALUES (%(name)s, %(time)s, %(servings)s, %(instructions)s, %(source)s, %(rating)s)
            RETURNING id
        """, recipe)
        recipe_id, = cur.fetchone()
        app.logger.debug("Created recipe: " + str(recipe_id))

        for tag_id in tag_ids:
            cur.execute("""
                INSERT INTO tag_recipe_edges (tag_id, recipe_id)
                VALUES (%s, %s)
            """, [tag_id, recipe_id])
        app.logger.debug("Inserted tag edges")

        for ing_desc in recipe.get("ingredients", []):
            cur.execute("""
                INSERT INTO recipe_ingredient_edges (recipe_id, ingredient_id, quantity, unit_id)
                VALUES (%s, %s, %s, %s)
            """, [
                recipe_id,
                ingredient_to_id[ing_desc["ingredient"]],
                ing_desc["quantity"],
                unit_to_id[ing_desc["unit"]]
            ])
        app.logger.debug("Inserted tag edges")

        conn.commit()
        cur.close()

        return get_formatted_recipe(db, recipe_id), 200
    elif request.method == 'GET':
        # Get list of recipes, potentially filtered by the query parameter
        # No query results in querying all recipes
        query = request.args.get('q')
        if query:
            return "Query parameters not supported", 400
        
        recipes = get_all_formatted_recipes(db)

        return {"recipes": recipes}, 200
    else:
        return "Bad request", 405

@app.route('/recipe/<recipe_id>', methods = ['GET', 'PUT', 'DELETE'])
def recipe(recipe_id):
    if request.method == 'GET':
        # Read a recipe
        raise NotImplementedError
    elif request.method == 'PUT':
        data = request.form
        # Update a recipe
        raise NotImplementedError
    elif request.method == 'DELETE':
        # Delete a recipe
        raise NotImplementedError
    else:
        raise NotImplementedError

@app.route('/planner/generate', methods = ['POST'])
def meal_planner_generate_plan():
    ''' Returns a meal plan and grocery list based on the
        supplied criteria
    '''
    if request.method == 'POST':
        planner_params = PlannerParams() # TODO - parse parameters from the user
        if not verify_parameters(planner_params):
            return "Conflicting meal planner parameters", 400

        recipes = get_all_formatted_recipes(db)
        ingredients = get_all_ingredients_with_location(db)
        meal_plan = generate_meal_plan(recipes, PlannerParams())
        grocery_list = generate_grocery_list(meal_plan, ingredients)

        return {"grocery_list": grocery_list, "meal_plan": meal_plan}, 200
    else:
        return "Bad request", 405
