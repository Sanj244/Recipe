from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "<api key>"
BASE_URL = "https://api.spoonacular.com/recipes/"

def get_recipes_by_ingredients(ingredients, max_missing_ingredients=2, number_of_recipes=5):
    url = f"{BASE_URL}findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": number_of_recipes,
        "apiKey": API_KEY,
        "maxMissingIngredients": max_missing_ingredients
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_recipe_details(recipe_id):
    url = f"{BASE_URL}{recipe_id}/information"
    params = {
        "apiKey": API_KEY,
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        
        recipes = get_recipes_by_ingredients(ingredients)
        
        if recipes:
            recommendations = []
            for recipe in recipes:
                recipe_id = recipe["id"]
                recipe_details = get_recipe_details(recipe_id)
                if recipe_details:
                    recommendations.append({
                        "title": recipe_details["title"],
                        "image": recipe_details["image"],
                        "ingredients": [ingredient["name"] for ingredient in recipe_details["extendedIngredients"]],
                        "instructions": recipe_details["instructions"]
                    })
            return render_template("index.html", recipes=recommendations, ingredients=ingredients)
        else:
            error_message = "Sorry, no recipes found."
            return render_template("index.html", error_message=error_message)
    
    return render_template("index.html", recipes=None)

if __name__ == "__main__":
    app.run(debug=True)
