def touch_tag(app, cur, tag):
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

def touch_ingredient(app, cur, ingredient):
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

def touch_unit(app, cur, unit):
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