# Development Guide

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Basic understanding of Flask and WebSockets

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Chatbot-E-commerce-Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## Project Architecture

### Backend Components

#### ChatbotEngine (`src/chatbot/engine.py`)
- Handles natural language processing
- Intent recognition using regex patterns
- Manages conversation context per user
- Generates appropriate responses

**Key Methods:**
- `process_message(message, user_id)` - Main entry point for chat
- `_match_intent(message)` - Finds matching intent
- `_generate_response(intent, message)` - Creates response

#### ProductCatalog (`src/models/product_catalog.py`)
- Manages product inventory
- Search and filtering capabilities
- Category management

**Key Methods:**
- `search_products(query)` - Text-based search
- `get_product_by_id(id)` - Retrieve specific product
- `get_products_by_category(category)` - Filter by category

#### Flask Application (`app.py`)
- REST API endpoints
- WebSocket event handlers
- Server configuration

### Frontend Components

#### HTML (`templates/index.html`)
- Main chat interface
- Product sidebar
- Quick action buttons

#### CSS (`static/css/style.css`)
- Modern gradient design
- Responsive layout
- Animation effects

#### JavaScript (`static/js/app.js`)
- Socket.IO integration
- Message handling
- Product display

## Adding New Features

### Adding New Intents

1. Edit `src/chatbot/engine.py`
2. Add new intent to `_load_intents()` method:

```python
"new_intent_name": {
    "patterns": [
        r"\b(keyword1|keyword2)\b",
        r"\b(another pattern)\b",
    ],
    "responses": [
        "Response option 1",
        "Response option 2",
    ]
}
```

### Adding Products

Edit `src/models/product_catalog.py` in the `_load_sample_products()` method:

```python
{
    "id": "PROD009",
    "name": "New Product",
    "category": "Category",
    "price": 99.99,
    "description": "Product description",
    "stock": 100,
    "image_url": "/static/images/product.jpg"
}
```

### Adding API Endpoints

Add new routes in `app.py`:

```python
@app.route('/api/new-endpoint')
def new_endpoint():
    # Your logic here
    return jsonify({"result": "data"})
```

## Testing

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_chatbot.py

# Verbose output
python -m unittest discover tests/ -v
```

### Writing Tests

Create test files in `tests/` directory:

```python
import unittest
from src.chatbot.engine import ChatbotEngine

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.chatbot = ChatbotEngine()
    
    def test_something(self):
        result = self.chatbot.process_message("test")
        self.assertIsNotNone(result)
```

## Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```bash
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

### Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for configuration
3. **Disable debug mode** in production
4. **Bind to localhost** (127.0.0.1) for development
5. **Use HTTPS** in production

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

**Socket.IO not connecting:**
- Check if CDN is accessible
- Verify CORS settings
- Check browser console for errors

**Products not loading:**
- Check API endpoint: `http://localhost:5000/api/products`
- Verify product catalog initialization

**Tests failing:**
- Ensure all dependencies are installed
- Check Python version (3.8+)
- Verify file paths are correct

## Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings to all functions/classes
- Keep functions focused and small
- Write descriptive variable names

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Deployment

### Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use secure `SECRET_KEY`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Backup strategy

### Using Gunicorn

```bash
pip install gunicorn eventlet
gunicorn -k eventlet -w 1 app:app --bind 0.0.0.0:8000
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Socket.IO Documentation](https://socket.io/docs/)
- [Python unittest](https://docs.python.org/3/library/unittest.html)

## Support

For questions or issues:
- Check existing GitHub issues
- Review documentation
- Contact the development team
