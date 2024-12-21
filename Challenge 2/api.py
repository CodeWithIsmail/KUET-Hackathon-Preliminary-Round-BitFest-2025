from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["recipe_manager"]
ingredients_collection = db["ingredients"]
recipes_collection = db["recipes"]

# Helper function to get current timestamp
def get_timestamp():
    return datetime.utcnow().isoformat()

# 1. Add or Update Ingredients
@app.route('/api/ingredients', methods=['POST'])
def add_update_ingredient():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")
    unit = data.get("unit")

    if not name or not quantity or not unit:
        return jsonify({"error": "Missing fields: name, quantity, or unit"}), 400

    ingredients_collection.update_one(
        {"name": name},
        {"$set": {"quantity": quantity, "unit": unit, "updated_at": get_timestamp()}},
        upsert=True
    )

    return jsonify({"message": "Ingredient added/updated successfully."}), 200

# 2. Get All Ingredients
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = list(ingredients_collection.find({}, {"_id": 0}))
    return jsonify(ingredients), 200

# 3. Delete Ingredient
@app.route('/api/ingredients/<name>', methods=['DELETE'])
def delete_ingredient(name):
    result = ingredients_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        return jsonify({"error": "Ingredient not found."}), 404
    return jsonify({"message": "Ingredient deleted successfully."}), 200

# 4. Add Recipe
@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    title = data.get("title")
    ingredients = data.get("ingredients")
    taste = data.get("taste")
    cuisine = data.get("cuisine")
    preparation_time = data.get("preparation_time")
    reviews = data.get("reviews")
    instructions = data.get("instructions")

    if not title or not ingredients or not instructions:
        return jsonify({"error": "Missing fields: title, ingredients, or instructions"}), 400

    recipe = {
        "title": title,
        "ingredients": ingredients,
        "taste": taste,
        "cuisine": cuisine,
        "preparation_time": preparation_time,
        "reviews": reviews,
        "instructions": instructions
    }
    recipes_collection.insert_one(recipe)
    return jsonify({"message": "Recipe added successfully."}), 201

# 5. Get Recipes
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = list(recipes_collection.find({}, {"_id": 0}))
    return jsonify(recipes), 200

# 6. Chatbot Endpoint
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    preference = data.get("preference")
    available_ingredients = data.get("available_ingredients")

    if not preference or not available_ingredients:
        return jsonify({"error": "Missing fields: preference or available_ingredients"}), 400

    matching_recipes = recipes_collection.find({"taste": preference})
    for recipe in matching_recipes:
        if all(ing["name"] in available_ingredients for ing in recipe["ingredients"]):
            return jsonify({
                "response": f"Try making {recipe['title']}! Ingredients: {recipe['ingredients']}. Instructions: {recipe['instructions']}"
            }), 200

    return jsonify({"response": "No matching recipes found."}), 200

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
