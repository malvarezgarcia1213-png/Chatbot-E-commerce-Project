# E-commerce Chatbot Project

An intelligent AI-powered chatbot designed to enhance E-commerce customer experience, increase sales, and improve customer satisfaction. This chatbot can be integrated into any online shop to provide 24/7 customer support.

## 🌟 Features

- **Intelligent Conversations**: Natural language processing to understand customer queries
- **Product Search & Recommendations**: Help customers find products based on their needs
- **Order Tracking**: Assist customers in tracking their orders
- **Customer Support**: Answer FAQs about shipping, returns, payments, and more
- **Real-time Chat**: WebSocket-based real-time communication
- **Product Catalog Management**: Browse and search through product inventory
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/malvarezgarcia1213-png/Chatbot-E-commerce-Project.git
   cd Chatbot-E-commerce-Project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to: `http://localhost:5000`

## 📁 Project Structure

```
Chatbot-E-commerce-Project/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup file
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── chatbot/               # Chatbot logic
│   │   ├── __init__.py
│   │   └── engine.py          # Core chatbot engine
│   └── models/                # Data models
│       ├── __init__.py
│       └── product_catalog.py # Product management
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Stylesheets
│   └── js/
│       └── app.js             # Frontend JavaScript
│
├── templates/                  # HTML templates
│   └── index.html             # Main chat interface
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_chatbot.py        # Chatbot tests
│   └── test_product_catalog.py # Product catalog tests
│
├── data/                       # Data files
│   └── products/              # Product data
│
└── config/                     # Configuration files
```

## 🎯 Chatbot Capabilities

The chatbot can handle various customer queries including:

1. **Greetings & Welcome**
   - "Hello", "Hi", "Good morning"

2. **Product Search**
   - "I'm looking for shoes"
   - "Show me electronics"
   - "Do you have laptops?"

3. **Price Inquiries**
   - "How much does it cost?"
   - "What's the price?"

4. **Order Tracking**
   - "Track my order"
   - "Where is my package?"

5. **Shopping Cart**
   - "Add to cart"
   - "Checkout"

6. **Shipping Information**
   - "How long will delivery take?"
   - "What are shipping options?"

7. **Returns & Refunds**
   - "What's your return policy?"
   - "How do I return an item?"

8. **Payment Methods**
   - "What payment methods do you accept?"
   - "Can I pay with PayPal?"

9. **Product Recommendations**
   - "What do you recommend?"
   - "Show me best sellers"

10. **Customer Support**
    - "Contact support"
    - "Speak to a human"

## 🔧 API Endpoints

### REST API

- `GET /api/health` - Health check endpoint
- `POST /api/chat` - Send a message to the chatbot
  ```json
  {
    "message": "Hello",
    "user_id": "optional_user_id"
  }
  ```
- `GET /api/products` - Get all products
- `GET /api/products?q=search_term` - Search products
- `GET /api/products/{id}` - Get specific product
- `GET /api/categories` - Get all product categories

### WebSocket Events

- `connect` - Client connects to server
- `send_message` - Send a message to chatbot
- `receive_message` - Receive response from chatbot
- `disconnect` - Client disconnects

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_chatbot.py

# Run with coverage
python -m pytest tests/ --cov=src

# Or use unittest
python -m unittest discover tests/
```

## 🎨 Customization

### Adding New Intents

Edit `src/chatbot/engine.py` to add new conversation intents:

```python
"new_intent": {
    "patterns": [
        r"\b(pattern1|pattern2)\b",
    ],
    "responses": [
        "Response 1",
        "Response 2",
    ]
}
```

### Adding Products

Products can be added by modifying the `_load_sample_products()` method in `src/models/product_catalog.py` or by loading from a JSON file.

### Styling

Customize the appearance by editing `static/css/style.css`.

## 🚀 Deployment

### Deploy to Production

1. Update the secret key in `app.py`:
   ```python
   app.config['SECRET_KEY'] = 'your-production-secret-key'
   ```

2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -k eventlet -w 1 app:app
   ```

3. Set up a reverse proxy (nginx, Apache)

4. Configure SSL/TLS for HTTPS

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t ecommerce-chatbot .
docker run -p 5000:5000 ecommerce-chatbot
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- E-commerce Chatbot Team

## 🙏 Acknowledgments

- Built with Flask, Socket.IO, and modern web technologies
- Designed to improve E-commerce customer experience
- Focused on increasing sales and customer satisfaction

## 📞 Support

For support, email support@ecommerce.com or open an issue in the repository.

## 🔮 Future Enhancements

- [ ] Integration with machine learning models for better intent recognition
- [ ] Multi-language support
- [ ] Voice chat capability
- [ ] Integration with popular E-commerce platforms (Shopify, WooCommerce)
- [ ] Advanced analytics and reporting
- [ ] Customer sentiment analysis
- [ ] Automated product recommendations using ML
- [ ] Integration with payment gateways
- [ ] Order management system
- [ ] Admin dashboard for chatbot management

---

**Made with ❤️ for better E-commerce experiences**
