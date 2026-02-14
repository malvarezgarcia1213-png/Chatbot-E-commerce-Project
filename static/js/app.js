// E-commerce Chatbot - Frontend JavaScript

class ChatbotApp {
    constructor() {
        this.socket = null;
        this.userId = this.generateUserId();
        this.init();
    }

    generateUserId() {
        // Generate a user ID for session tracking
        // Try to use crypto.randomUUID() if available, otherwise fallback
        if (typeof crypto !== 'undefined' && crypto.randomUUID) {
            return 'user_' + crypto.randomUUID();
        }
        // Fallback: timestamp + random string for better uniqueness
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    init() {
        // Initialize WebSocket connection
        this.initializeSocket();
        
        // Load products
        this.loadProducts();
        
        // Set up event listeners
        this.setupEventListeners();
    }

    initializeSocket() {
        // Connect to Socket.IO server
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to chatbot server');
        });

        this.socket.on('connected', (data) => {
            console.log(data.message);
        });

        this.socket.on('receive_message', (data) => {
            this.displayBotMessage(data);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
    }

    setupEventListeners() {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('user-input');
        const quickActions = document.querySelectorAll('.quick-action');

        // Handle form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = input.value.trim();
            if (message) {
                this.sendMessage(message);
                input.value = '';
            }
        });

        // Handle quick action buttons
        quickActions.forEach(button => {
            button.addEventListener('click', () => {
                const message = button.getAttribute('data-message');
                this.sendMessage(message);
            });
        });
    }

    sendMessage(message) {
        // Display user message
        this.displayUserMessage(message);

        // Send message via WebSocket
        this.socket.emit('send_message', {
            message: message,
            user_id: this.userId
        });
    }

    displayUserMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    displayBotMessage(data) {
        const messagesContainer = document.getElementById('chat-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        let content = `<p>${this.escapeHtml(data.response)}</p>`;
        
        // Display products if available
        if (data.products && data.products.length > 0) {
            content += '<div class="product-results">';
            data.products.forEach(product => {
                content += `
                    <div class="product-item">
                        <h5>${this.escapeHtml(product.name)}</h5>
                        <p>${this.escapeHtml(product.description)}</p>
                        <p class="product-price">$${product.price.toFixed(2)}</p>
                    </div>
                `;
            });
            content += '</div>';
        }
        
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                ${content}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    async loadProducts() {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            if (data.products) {
                this.displayProducts(data.products);
            }
        } catch (error) {
            console.error('Error loading products:', error);
            const productList = document.getElementById('product-list');
            productList.innerHTML = '<div class="loading">Failed to load products</div>';
        }
    }

    displayProducts(products) {
        const productList = document.getElementById('product-list');
        productList.innerHTML = '';
        
        // Display first 6 products
        const displayProducts = products.slice(0, 6);
        
        displayProducts.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <h4>${this.escapeHtml(product.name)}</h4>
                <p class="category">${this.escapeHtml(product.category)}</p>
                <p class="price">$${product.price.toFixed(2)}</p>
            `;
            
            productCard.addEventListener('click', () => {
                this.sendMessage(`Tell me about ${product.name}`);
            });
            
            productList.appendChild(productCard);
        });
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotApp();
});
