from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to MealPlanner!'

@app.route('/ingredient/create', methods = ['POST'])
def ingredient_create():
    if request.method == 'POST':
        data = request.form
        # todo
    else:
        # todo raise error

@app.route('/ingredient/update/<ingredient_id>', methods = ['GET', 'POST', 'DELETE'])
def ingredient_update(ingredient_id):
    if request.method == 'GET':
        # todo
    elif request.method == 'POST':
        data = request.form
        # todo
    elif request.method == 'DELETE':
        # todo
    else:
        # todo raise error

@app.route('/ingredient/search/name/<ingredient_name>', methods = ['GET'])
def ingredient_search_name(ingredient_name):
    if request.method == 'GET':
        # todo
    else:
        # todo raise error

@app.route('/ingredient/search/all', methods = ['GET'])
def ingredient_search_all(ingredient_name):
    ''' Get all of the available ingredients
    '''
    if request.method == 'GET':
        # todo
    else:
        # todo raise error

@app.route('/recipe/create', methods = ['POST'])
def recipe_create():
    if request.method == 'POST':
        data = request.form
        # todo
    else:
        # todo raise error

@app.route('/recipe/update/<recipe_id>', methods = ['GET', 'POST', 'DELETE'])
def recipe_update(recipe_id):
    if request.method == 'GET':
        # todo
    elif request.method == 'POST':
        data = request.form
        # todo
    elif request.method == 'DELETE':
        # todo
    else:
        # todo raise error

@app.route('/recipe/search/name/<recipe_name>', methods = ['GET'])
def recipe_search_name(recipe_name):
    if request.method == 'GET':
        # todo
    else:
        # todo raise error

@app.route('/recipe/search/all', methods = ['GET'])
def recipe_search_all(recipe_name):
    ''' Get all of the available recipes
    '''
    if request.method == 'GET':
        # todo
    else:
        # todo raise error

@app.route('/planner/generate', methods = ['POST'])
def meal_planner_generate_plan():
    ''' Returns a meal plan and grocery list based on the
        supplied criteria
    '''
    if request.method == 'POST':
        data = request.form
        # todo
    else:
        # todo raise error
