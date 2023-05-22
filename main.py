import os
import re
from numpy import rec
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import random
from config import API_KEY

# initialize OpenAI API
openai.api_key = API_KEY

meals = {
    'vegetarian': [
        'vegetarian pasta dinner',
        'vegetarian stir-fry dinner',
        'vegetarian curry dinner',
        'vegetarian Buddha bowl',
        'vegetarian salad dinner'
    ],
    'chicken': [
        'grilled chicken dinner',
        'baked chicken dinner',
        'chicken salad dinner',
        'chicken stir-fry dinner',
        'chicken and vegetable soup'
    ],
    'fish': [
        'grilled fish dinner',
        'pan-seared fish dinner',
        'fish and vegetable stew',
        'fish taco dinner',
        'fish salad dinner'
    ],
    'generic': [
        'rice and vegetable stir-fry',
        'pasta primavera',
        'quinoa salad',
        'stuffed bell peppers',
        'black bean tacos',
        'vegetable curry',
        'roasted vegetable medley',
        'tofu stir-fry',
        'bean and vegetable soup',
        'grain bowl with roasted veggies'
    ],
    'comfort_dinner': [
        'macaroni and cheese',
        'chicken pot pie',
        'beef stew',
        'grilled cheese sandwich',
        'mashed potatoes with gravy',
        'chicken and dumplings',
        'meatloaf',
        'chili con carne',
        'beef lasagna',
        'chicken parmigiana',
        'fish and chips'
    ]
}

# function to generate recipe
def generate_recipe(meal):
    prompt = f"""
    Act like my nutritionist and fitness coach.
    I want you to generate a recipe with Ingrediens and Instructions.

    Create a healthy, {meal}  recipe for a young active, fitness-conscious couple.
    The meal should contain a balance of protein, carbs, and fresh vegetables.
    The recipe should be in the following format:

    (Please include a short and catchy name for the recipe)
    Recipe Name: exemple : f{meal}

    (Specify the number of servings the recipe yields)
    Serving Size:
    exemple : 4 servings

    Ingredients:

    Ingredients:
    (List all ingredients required for the recipe. Please specify quantities or measures for each ingredient.)
    - Ingredient 1
    - Ingredient 2
    - Ingredient 3
    ...
 
    Instructions:
    (List all steps required to make the recipe. Please use a number for each step.)
    1. Step 1
    2. Step 2
    3. Step 3
    ...
    """

    response = openai.Completion.create(
        engine="text-davinci-002",  # use OpenAI's largest language model
        prompt=prompt,
        temperature=0.3,
        max_tokens=1000,
    )
    print(response)
    recipe_text = response['choices'][0]['text'].strip()
    return recipe_text

# function to extract recipe details
# function to extract recipe details
# function to extract recipe details
def extract_recipe_details(recipe_text):
    recipe_lines = recipe_text.split('\n')
    recipe_name = ''
    serving_size = ''
    ingredients = []
    instructions = []

    # Extract recipe name and serving size
    for line in recipe_lines:
        if line.startswith("Recipe Name:"):
            recipe_name = line.replace("Recipe Name:", "").strip()
        elif line.startswith("Serving"):
            serving_size = line.replace("Serving Size:", "").strip()

    # Extract ingredients
    try:
        ingredient_start_index = next(i for i, line in enumerate(recipe_lines) if line.strip() == "Ingredients:") + 1
        ingredient_end_index = next(i for i, line in enumerate(recipe_lines) if line.strip() == "Instructions:")
        for i in range(ingredient_start_index, ingredient_end_index):
            ingredient = recipe_lines[i].strip()
            if ingredient and ingredient.startswith('-'):  # Check if the line starts with '-'
                ingredient = ingredient.replace('-', '', 1).strip()  # Remove the '-' character
                ingredients.append(ingredient)
    except StopIteration:
        print("Failed to extract ingredients. Please re-enter the recipe.")
        

    # Extract instructions
    try:
        instructions_start_index = next(i for i, line in enumerate(recipe_lines) if line.strip() == "Instructions:") + 1
        for i in range(instructions_start_index, len(recipe_lines)):
            instruction = recipe_lines[i].strip()
            if instruction:  # Accept any non-empty line as an instruction
                # Remove the number and dot at the beginning of each instruction if present
                instruction = re.sub(r'^\d+\.\s*', '', instruction)
                instructions.append(instruction)
    except StopIteration:
        print("Failed to extract instructions. Please re-enter the recipe.")
        


    recipe_details = {
        'name': recipe_name,
        'serving_size': serving_size,
        'ingredients': ingredients,
        'instructions': instructions 
    }

    return recipe_details


# function to save recipe to file
def save_recipe_to_file(recipe_details, directory_path):
    # sanitize the recipe name to create a valid filename
    file_name = "".join(c for c in recipe_details['name'] if c.isalnum() or c.isspace()).rstrip() + ".txt"
    
    # create the full file path
    file_path = os.path.join(directory_path, file_name)

    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as file:
        file.write(f"Recipe Name: {recipe_details['name']}\n\n")
        file.write(f"Serving Size: {recipe_details['serving_size']}\n\n")
        file.write("Ingredients:\n")
        for ingredient in recipe_details['ingredients']:
            file.write(f"{ingredient}\n")
        file.write("\nInstructions:\n")
        for i, instruction in enumerate(recipe_details['instructions'], start=1):
            file.write(f"{i}. {instruction}\n")


