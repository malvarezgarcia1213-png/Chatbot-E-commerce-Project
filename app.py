"""
E-commerce Chatbot Web Application
Flask server with REST API and WebSocket support
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.engine import ChatbotEngine
from models.product_catalog import ProductCatalog

# Initialize Flask app
app = Flask(__name__)
# Load secret key from environment or use a secure default for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize chatbot engine and product catalog
chatbot = ChatbotEngine()
product_catalog = ProductCatalog()

@app.route('/')
def index():
    """Render main chat interface"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "E-commerce Chatbot"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    REST API endpoint for chat messages
    
    Expected JSON: {"message": "user message", "user_id": "optional_user_id"}
    Returns: {"response": "bot response", "intent": "detected_intent", ...}
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Process message through chatbot
        result = chatbot.process_message(message, user_id)
        
        # Check if user is asking about products
        if result['intent'] in ['product_search', 'recommendations']:
            # Extract keywords for product search
            keywords = message.lower()
            products = product_catalog.search_products(keywords)
            
            if products:
                product_list = [p.to_dict() for p in products[:5]]  # Limit to 5
                result['products'] = product_list
                result['response'] += f"\n\nI found {len(products)} products that might interest you!"
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products or search products"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if query:
        products = product_catalog.search_products(query)
    elif category:
        products = product_catalog.get_products_by_category(category)
    else:
        products = product_catalog.get_all_products()
    
    return jsonify({
        "products": [p.to_dict() for p in products],
        "count": len(products)
    })

@app.route('/api/products/<product_id>')
def get_product(product_id):
    """Get specific product by ID"""
    product = product_catalog.get_product_by_id(product_id)
    
    if product:
        return jsonify(product.to_dict())
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/api/categories')
def get_categories():
    """Get all product categories"""
    categories = product_catalog.get_all_categories()
    return jsonify({"categories": categories})

# WebSocket events for real-time chat
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'message': 'Connected to chatbot server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('send_message')
def handle_message(data):
    """
    Handle incoming WebSocket message
    
    Expected data: {"message": "user message", "user_id": "optional_user_id"}
    """
    message = data.get('message', '')
    user_id = data.get('user_id', 'default')
    
    if message:
        # Process message through chatbot
        result = chatbot.process_message(message, user_id)
        
        # Check for product-related queries
        if result['intent'] in ['product_search', 'recommendations']:
            keywords = message.lower()
            products = product_catalog.search_products(keywords)
            
            if products:
                product_list = [p.to_dict() for p in products[:5]]
                result['products'] = product_list
                result['response'] += f"\n\nI found {len(products)} products for you!"
        
        # Send response back to client
        emit('receive_message', result)

if __name__ == '__main__':
    print("=" * 60)
    print("E-commerce Chatbot Server Starting...")
    print("=" * 60)
    print("Server will be available at: http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /api/health - Health check")
    print("  - POST /api/chat - Send chat message")
    print("  - GET  /api/products - Get products")
    print("  - GET  /api/categories - Get categories")
    print("=" * 60)
    print("WARNING: Running in development mode. Do not use in production!")
    print("=" * 60)
    
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')  # Default to localhost for security
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    socketio.run(app, debug=debug_mode, host=host, port=port, allow_unsafe_werkzeug=True)
