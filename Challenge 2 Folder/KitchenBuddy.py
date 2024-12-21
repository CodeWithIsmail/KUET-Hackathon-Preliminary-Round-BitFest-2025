from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import google.generativeai as genai

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

# Helper function to extract preference from user message
def extract_preference(message):
    # Simplified example - this can be expanded based on message content
    preferences = ["sweet", "savory", "spicy", "salty"]
    for pref in preferences:
        if pref in message.lower():
            return pref
    return "any"  # Default if no specific preference is found

# Helper function to extract ingredients from user message
def extract_ingredients(message):
    # Simplified example - ideally, you would use NLP to detect ingredients
    ingredients = ["egg", "flour", "sugar", "butter", "milk", "vanilla", "chocolate", "salt"]
    available_ingredients = [ingredient for ingredient in ingredients if ingredient in message.lower()]
    return available_ingredients

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
    user_message = data.get("message")  # User's complex input (e.g., "Can I make a cake with eggs and flour?")

    if not user_message:
        return jsonify({"error": "Missing field: message"}), 400

    # Extract preferences and ingredients from the user message
    preference = extract_preference(user_message)  # Extract preference like sweet, savory, etc.
    available_ingredients = extract_ingredients(user_message)  # Extract ingredients mentioned in the message

    # Send the user message to Gemini for further interpretation (if needed)
    chat = genai.GenerativeModel("gemini-1.5-flash")
    response = chat.start_chat(
        history=[
            {"role": "user", "parts": user_message}
        ]
    )

    # Get the response from Gemini
    response_text = ""
    for chunk in response:
        response_text += chunk.text

    # Fetch recipes based on preference and available ingredients
    matching_recipes = recipes_collection.find({"taste": {"$regex": preference, "$options": "i"}})

    recipe_recommendations = []
    for recipe in matching_recipes:
        # Check if all ingredients required for the recipe are available in the pantry
        recipe_ingredients = [ing["name"] for ing in recipe["ingredients"]]
        if all(ingredient in available_ingredients for ingredient in recipe_ingredients):
            recipe_recommendations.append({
                "title": recipe["title"],
                "ingredients": recipe["ingredients"],
                "instructions": recipe["instructions"]
            })

    if recipe_recommendations:
        return jsonify({
            "response": f"Here are some recipes you can try based on your preferences: {recipe_recommendations}"
        }), 200
    else:
        return jsonify({"response": "Sorry, we couldn't find any recipes that match your preferences."}), 200

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)