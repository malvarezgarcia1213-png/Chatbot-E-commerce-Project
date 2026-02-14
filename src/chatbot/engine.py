"""
Core Chatbot Engine
Handles natural language processing and response generation
"""

import re
import json
from typing import Dict, List, Tuple, Any
import random


class ChatbotEngine:
    """
    Main chatbot engine that processes user messages and generates responses
    """
    
    def __init__(self):
        """Initialize the chatbot engine with intents and patterns"""
        self.intents = self._load_intents()
        self.context = {}
        
    def _load_intents(self) -> Dict:
        """Load chatbot intents and response patterns"""
        return {
            "greeting": {
                "patterns": [
                    r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b",
                ],
                "responses": [
                    "Hello! Welcome to our store. How can I help you today?",
                    "Hi there! I'm here to help you find what you're looking for.",
                    "Greetings! How may I assist you with your shopping today?",
                ]
            },
            "product_search": {
                "patterns": [
                    r"\b(looking for|search|find|show me|want to buy|need|interested in)\b.*\b(product|item|shirt|shoe|dress|pants|jacket|electronics|phone|laptop)\b",
                    r"\b(do you have|sell|offer|available)\b",
                ],
                "responses": [
                    "I'd be happy to help you find products! What specific item are you looking for?",
                    "Let me help you search our catalog. Can you tell me more about what you need?",
                    "Sure! I can help you find the perfect item. What category are you interested in?",
                ]
            },
            "price_inquiry": {
                "patterns": [
                    r"\b(price|cost|how much|expensive|cheap|affordable)\b",
                ],
                "responses": [
                    "Our prices are competitive and we offer great value! What product would you like to know the price of?",
                    "I can help you with pricing information. Which item are you interested in?",
                    "We have products at various price points to fit every budget. What are you looking for?",
                ]
            },
            "order_status": {
                "patterns": [
                    r"\b(order|track|status|where is my|shipping|delivery|tracking number)\b",
                ],
                "responses": [
                    "I can help you track your order. Please provide your order number.",
                    "Let me check your order status for you. What's your order number?",
                    "I'll be happy to help track your order. Could you share your order ID?",
                ]
            },
            "cart_help": {
                "patterns": [
                    r"\b(cart|add to cart|shopping cart|checkout|buy now|purchase)\b",
                ],
                "responses": [
                    "I can help you with your shopping cart. Would you like to add items or proceed to checkout?",
                    "Ready to make a purchase? I can guide you through adding items to cart and checkout.",
                    "Let me assist you with your cart. What would you like to do?",
                ]
            },
            "return_policy": {
                "patterns": [
                    r"\b(return|refund|exchange|warranty|guarantee|policy)\b",
                ],
                "responses": [
                    "We offer a 30-day return policy on most items. Would you like more details?",
                    "Our return policy is customer-friendly! You can return items within 30 days of purchase.",
                    "We want you to be satisfied! Returns are accepted within 30 days with original packaging.",
                ]
            },
            "payment_methods": {
                "patterns": [
                    r"\b(payment|pay|credit card|debit|paypal|visa|mastercard|payment method)\b",
                ],
                "responses": [
                    "We accept all major credit cards, debit cards, and PayPal. Shop with confidence!",
                    "You can pay using credit/debit cards (Visa, Mastercard, Amex) or PayPal.",
                    "Multiple payment options available: credit cards, debit cards, and PayPal.",
                ]
            },
            "shipping_info": {
                "patterns": [
                    r"\b(shipping|delivery time|how long|when will|arrive|ship)\b",
                ],
                "responses": [
                    "Standard shipping takes 3-5 business days. Express shipping is also available!",
                    "We offer multiple shipping options: Standard (3-5 days) and Express (1-2 days).",
                    "Your order will typically arrive within 3-5 business days with standard shipping.",
                ]
            },
            "recommendations": {
                "patterns": [
                    r"\b(recommend|suggest|popular|best seller|trending|what should i buy)\b",
                ],
                "responses": [
                    "I'd love to recommend products! What category interests you - electronics, clothing, accessories?",
                    "Our best sellers are quite popular! What type of product are you interested in?",
                    "Based on customer reviews, I can suggest our top-rated items. What are you shopping for?",
                ]
            },
            "contact_support": {
                "patterns": [
                    r"\b(contact|support|help|speak to|human|agent|representative)\b",
                ],
                "responses": [
                    "For additional support, you can reach our team at support@ecommerce.com or call 1-800-SHOP-NOW.",
                    "Need to speak with a human? Contact us at support@ecommerce.com or call 1-800-SHOP-NOW.",
                    "Our support team is available at support@ecommerce.com or phone: 1-800-SHOP-NOW.",
                ]
            },
            "farewell": {
                "patterns": [
                    r"\b(bye|goodbye|see you|thanks|thank you|that's all)\b",
                ],
                "responses": [
                    "Thank you for shopping with us! Have a great day!",
                    "Goodbye! Feel free to return if you need any help. Happy shopping!",
                    "Thanks for visiting! We're here 24/7 if you need assistance. Take care!",
                ]
            },
            "default": {
                "patterns": [],
                "responses": [
                    "I'm here to help with your shopping needs! Could you please rephrase your question?",
                    "I want to assist you better. Can you provide more details about what you need?",
                    "I'm not sure I understood that. I can help with products, orders, shipping, and more!",
                ]
            }
        }
    
    def process_message(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Process incoming user message and generate response
        
        Args:
            message: User's message text
            user_id: Unique user identifier for context management
            
        Returns:
            Dictionary with response and metadata
        """
        message_lower = message.lower().strip()
        
        # Initialize user context if not exists
        if user_id not in self.context:
            self.context[user_id] = {"conversation_count": 0}
        
        self.context[user_id]["conversation_count"] += 1
        
        # Find matching intent
        intent, confidence = self._match_intent(message_lower)
        
        # Generate response
        response = self._generate_response(intent, message_lower)
        
        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "user_id": user_id
        }
    
    def _match_intent(self, message: str) -> Tuple[str, float]:
        """
        Match user message to an intent
        
        Args:
            message: User's message in lowercase
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        best_intent = "default"
        best_confidence = 0.0
        
        for intent_name, intent_data in self.intents.items():
            if intent_name == "default":
                continue
                
            for pattern in intent_data["patterns"]:
                if re.search(pattern, message, re.IGNORECASE):
                    # Simple confidence based on pattern match
                    confidence = 0.85 if len(message.split()) > 2 else 0.7
                    if confidence > best_confidence:
                        best_intent = intent_name
                        best_confidence = confidence
        
        return best_intent, best_confidence
    
    def _generate_response(self, intent: str, message: str) -> str:
        """
        Generate response based on matched intent
        
        Args:
            intent: Matched intent name
            message: Original user message
            
        Returns:
            Response string
        """
        if intent in self.intents:
            responses = self.intents[intent]["responses"]
            return random.choice(responses)
        
        return random.choice(self.intents["default"]["responses"])
    
    def reset_context(self, user_id: str):
        """Reset conversation context for a user"""
        if user_id in self.context:
            del self.context[user_id]
