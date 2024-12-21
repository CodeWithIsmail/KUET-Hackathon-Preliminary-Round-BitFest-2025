# KUET-Hackathon-Preliminary-Round-BitFest-2025

## API Documentation

### Route: /api/ingredients
-  Method: POST
-  Sample Payload:

```json
[
  {
    "name": "Tomato",
    "quantity": "2",
    "unit": "pieces"
  }
]
```

- Route: /api/ingredients
  Method: GET
  Sample Response:

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
