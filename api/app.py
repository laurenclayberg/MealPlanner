from flask import Flask, request
import json
from .db import db

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to MealPlanner!'

@app.route('/ingredients', methods = ['POST', 'GET'])
def ingredients():
    if request.method == 'POST':
        # Create a new ingredient
        raise NotImplementedError
    elif request.method == 'GET':
        # Search list of ingredients, potentially filtered by the query parameters
        # No query results in querying all ingredients
        query = request.args.get('q')
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

def touch_tag(cur, tag):
    app.logger.debug("Touch tag: " + str(tag))
    cur.execute("""
        INSERT INTO tags (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """, [tag])
    res = cur.fetchone()
    if res is None:
        cur.execute("""
            SELECT id FROM tags
            WHERE name = %s
            LIMIT 1
        """, [tag])
        res = cur.fetchone()
    tag_id, = res
    return tag_id

def touch_ingredient(cur, ingredient):
    app.logger.debug("Touch ingredient: " + str(ingredient))
    cur.execute("""
        INSERT INTO ingredients (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """, [ingredient])
    res = cur.fetchone()
    if res is None:
        cur.execute("""
            SELECT id FROM ingredients
            WHERE name = %s
            LIMIT 1
        """, [ingredient])
        res = cur.fetchone()
    ingredient_id, = res
    return ingredient_id

def touch_unit(cur, unit):
    app.logger.debug("Touch unit: " + str(unit))
    cur.execute("""
        INSERT INTO units (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """, [unit])
    res = cur.fetchone()
    if res is None:
        cur.execute("""
            SELECT id FROM units
            WHERE name = %s
            LIMIT 1
        """, [unit])
        res = cur.fetchone()
    unit_id, = res
    return unit_id

def get_formatted_recipe(recipe_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT pubid, name, time, servings, instructions, source, rating
        FROM recipes
        WHERE id = %s
        LIMIT 1;
    """, [recipe_id])
    recipe = {k: v for k, v in zip(["id", "name", "time", "servings", "instructions", "source", "rating"], cur.fetchone())}

    # Get tags
    cur.execute("""
        SELECT DISTINCT t.name
        FROM tag_recipe_edges tr
        INNER JOIN tags t ON t.id = tr.tag_id
        WHERE tr.recipe_id = %s;
    """, [recipe_id])
    recipe["tags"] = sorted(row[0] for row in cur.fetchall())

    # Get ingredients
    cur.execute("""
        SELECT
                i.name as ingredient,
                ri.quantity as quantity,
                u.name as unit
        FROM recipe_ingredient_edges ri
        INNER JOIN ingredients i ON i.id = ri.ingredient_id
        INNER JOIN units u ON u.id = ri.unit_id
        WHERE ri.recipe_id = %s;
    """, [recipe_id])
    recipe["ingredients"] = [
        {
            "ingredient": row[0],
            "quantity": row[1],
            "unit": row[2]
        } for row in cur.fetchall()
    ]
    cur.close()

    return recipe

@app.route('/recipes', methods = ['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        recipe = json.loads(request.data)
        # TODO: validate JSON using JSON schema
        conn = db()
        cur = conn.cursor()
        tag_ids = [touch_tag(cur, tag) for tag in sorted(set(recipe.get("tags", [])))]
        ingredient_to_id = {
            ing: touch_ingredient(cur, ing)
            for ing in sorted(set(
                ingredient_desc["ingredient"]
                for ingredient_desc in
                recipe.get("ingredients", [])
            ))
        }
        unit_to_id = {
            unit: touch_unit(cur, unit)
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

        return get_formatted_recipe(recipe_id)
    elif request.method == 'GET':
        # Get list of recipes, potentially filtered by the query parameter
        # No query results in querying all recipes
        query = request.args.get('q')
        if query:
            raise NotImplementedError
        cur = db().cursor()
        cur.execute("""
            SELECT
                r.pubid as id,
                r.time,
                r.servings,
                r.instructions,
                r.source,
                r.rating
            FROM recipes AS r
            ORDER BY r.created DESC;
            """)
        app.logger.debug(str(cur.fetchall()))
        raise NotImplementedError
    else:
        raise NotImplementedError

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
        raise NotImplementedError
    else:
        raise NotImplementedError
