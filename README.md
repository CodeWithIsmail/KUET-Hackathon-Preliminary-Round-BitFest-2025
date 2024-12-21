# KUET-Hackathon-Preliminary-Round-BitFest-2025

## Challenge-2 API Documentation

### Route: /api/ingredients

- Method: POST
- Sample Payload:

```json
[
  {
    "name": "Tomato",
    "quantity": "2",
    "unit": "pieces"
  }
]
```

### Route: /api/ingredients

- Method: GET
- Sample Response:

```json
[
  {
    "name": "Tomato",
    "quantity": "2",
    "unit": "pieces",
    "updated_at": "2024-12-23T12:34:56.789123"
  },
  {
    "name": "Onion",
    "quantity": "1",
    "unit": "kg",
    "updated_at": "2024-12-23T12:35:12.123456"
  }
]
```

### Route: /api/ingredients/<name>

- Method: DELETE
- Sample Response:

```json
{
  "message": "Ingredient deleted successfully."
}
```

### Route: /api/recipes

- Method: POST
- Sample Payload:

```json
{
  "title": "Tomato Soup",
  "ingredients": [
    { "name": "Tomato", "quantity": "2", "unit": "pieces" },
    { "name": "Onion", "quantity": "1", "unit": "piece" }
  ],
  "taste": "Spicy",
  "cuisine": "Indian",
  "preparation_time": "30 minutes",
  "reviews": "4.5",
  "instructions": "Boil tomatoes and onions, then blend together."
}
```

### Route: /api/recipes

- Method: GET
- Sample Response:

```json
[
  {
    "title": "Tomato Soup",
    "ingredients": [
      { "name": "Tomato", "quantity": "2", "unit": "pieces" },
      { "name": "Onion", "quantity": "1", "unit": "piece" }
    ],
    "taste": "Spicy",
    "cuisine": "Indian",
    "preparation_time": "30 minutes",
    "reviews": "4.5",
    "instructions": "Boil tomatoes and onions, then blend together."
  }
]
```

### Route: /api/chatbot

- Method: POST
- Sample Payload:

```json
{
  "preference": "Spicy",
  "available_ingredients": ["Tomato", "Onion"]
}
```
