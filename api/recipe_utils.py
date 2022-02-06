def get_formatted_recipe(db, recipe_id):
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

def get_all_recipe_ids(db):
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM recipes
    """)
    recipe_ids = [id_tuple[0] for id_tuple in cur.fetchall()]
    cur.close()
    return recipe_ids

def get_all_formatted_recipes(db):
    recipe_ids = get_all_recipe_ids(db)
    recipes = [get_formatted_recipe(db, recipe_id) for recipe_id in recipe_ids]
    return recipes
