import json
from flask import Flask, jsonify, render_template, request
from main import generate_recipe, extract_recipe_details, save_recipe_to_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get meal types from user input
    meals = request.form.getlist('meal')
    # Generate recipes and extract recipe details from recipe text 
    recipes = [extract_recipe_details(generate_recipe(meal)) for meal in meals]

    for i, recipe in enumerate(recipes, start=1):
        if recipe:
            recipe['id'] = i
        
    return render_template('recipe.html',recipes = recipes)



# @app.route('/grocery_list', methods=['GET'])
# def grocery_list():
#     recipes = request.args.get('recipes')
#     grocery_list = {}
#     for recipe in recipes:
#         for ingredient in recipe['ingredients']:
#             if ingredient in grocery_list:
#                 grocery_list[ingredient] += 1
#             else:
#                 grocery_list[ingredient] = 1
#     return render_template('grocery_list.html', grocery_list=grocery_list)



if __name__ == "__main__":
    app.run(debug=True)