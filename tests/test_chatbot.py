"""
Unit tests for ChatbotEngine
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot.engine import ChatbotEngine


class TestChatbotEngine(unittest.TestCase):
    """Test cases for ChatbotEngine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = ChatbotEngine()
    
    def test_initialization(self):
        """Test chatbot initializes correctly"""
        self.assertIsNotNone(self.chatbot)
        self.assertIsNotNone(self.chatbot.intents)
        self.assertIsInstance(self.chatbot.context, dict)
    
    def test_greeting_intent(self):
        """Test greeting intent recognition"""
        messages = ["Hello", "Hi", "Hey", "Good morning"]
        
        for message in messages:
            result = self.chatbot.process_message(message)
            self.assertEqual(result['intent'], 'greeting')
            self.assertIsInstance(result['response'], str)
            self.assertGreater(len(result['response']), 0)
    
    def test_product_search_intent(self):
        """Test product search intent recognition"""
        messages = [
            "I'm looking for shoes",
            "Show me laptops",
            "Do you have phones?",
            "I want to buy a shirt"
        ]
        
        for message in messages:
            result = self.chatbot.process_message(message)
            self.assertEqual(result['intent'], 'product_search')
            self.assertIsInstance(result['response'], str)
    
    def test_price_inquiry_intent(self):
        """Test price inquiry intent recognition"""
        messages = [
            "How much does it cost?",
            "What's the price?",
            "Is it expensive?"
        ]
        
        for message in messages:
            result = self.chatbot.process_message(message)
            self.assertEqual(result['intent'], 'price_inquiry')
            self.assertIsInstance(result['response'], str)
    
    def test_order_status_intent(self):
        """Test order status intent recognition"""
        messages = [
            "Track my order",
            "Where is my package?",
            "Order status"
        ]
        
        for message in messages:
            result = self.chatbot.process_message(message)
            self.assertEqual(result['intent'], 'order_status')
            self.assertIsInstance(result['response'], str)
    
    def test_farewell_intent(self):
        """Test farewell intent recognition"""
        messages = ["Goodbye", "Bye", "Thanks", "Thank you"]
        
        for message in messages:
            result = self.chatbot.process_message(message)
            self.assertEqual(result['intent'], 'farewell')
            self.assertIsInstance(result['response'], str)
    
    def test_default_intent(self):
        """Test default intent for unrecognized messages"""
        result = self.chatbot.process_message("xyzabc123")
        self.assertEqual(result['intent'], 'default')
        self.assertIsInstance(result['response'], str)
    
    def test_user_context(self):
        """Test user context management"""
        user_id = "test_user_123"
        
        # Send first message
        self.chatbot.process_message("Hello", user_id)
        self.assertIn(user_id, self.chatbot.context)
        self.assertEqual(self.chatbot.context[user_id]['conversation_count'], 1)
        
        # Send second message
        self.chatbot.process_message("Show me products", user_id)
        self.assertEqual(self.chatbot.context[user_id]['conversation_count'], 2)
    
    def test_reset_context(self):
        """Test context reset functionality"""
        user_id = "test_user_456"
        
        self.chatbot.process_message("Hello", user_id)
        self.assertIn(user_id, self.chatbot.context)
        
        self.chatbot.reset_context(user_id)
        self.assertNotIn(user_id, self.chatbot.context)
    
    def test_response_structure(self):
        """Test response structure contains all required fields"""
        result = self.chatbot.process_message("Hello")
        
        self.assertIn('response', result)
        self.assertIn('intent', result)
        self.assertIn('confidence', result)
        self.assertIn('user_id', result)
        
        self.assertIsInstance(result['response'], str)
        self.assertIsInstance(result['intent'], str)
        self.assertIsInstance(result['confidence'], float)
        self.assertIsInstance(result['user_id'], str)


if __name__ == '__main__':
    unittest.main()
