"""
Unit tests for ProductCatalog
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.product_catalog import Product, ProductCatalog


class TestProduct(unittest.TestCase):
    """Test cases for Product model"""
    
    def test_product_initialization(self):
        """Test product initialization"""
        product = Product(
            id="TEST001",
            name="Test Product",
            category="Test",
            price=99.99,
            description="A test product",
            stock=10
        )
        
        self.assertEqual(product.id, "TEST001")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.category, "Test")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.description, "A test product")
        self.assertEqual(product.stock, 10)
    
    def test_product_to_dict(self):
        """Test product to dictionary conversion"""
        product = Product(
            id="TEST001",
            name="Test Product",
            category="Test",
            price=99.99,
            description="A test product",
            stock=10
        )
        
        product_dict = product.to_dict()
        
        self.assertIsInstance(product_dict, dict)
        self.assertEqual(product_dict['id'], "TEST001")
        self.assertEqual(product_dict['name'], "Test Product")
        self.assertEqual(product_dict['price'], 99.99)
    
    def test_product_from_dict(self):
        """Test product creation from dictionary"""
        data = {
            "id": "TEST001",
            "name": "Test Product",
            "category": "Test",
            "price": 99.99,
            "description": "A test product",
            "stock": 10,
            "image_url": "/test.jpg"
        }
        
        product = Product.from_dict(data)
        
        self.assertEqual(product.id, "TEST001")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 99.99)


class TestProductCatalog(unittest.TestCase):
    """Test cases for ProductCatalog"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.catalog = ProductCatalog()
    
    def test_catalog_initialization(self):
        """Test catalog initializes with sample products"""
        self.assertIsNotNone(self.catalog)
        self.assertIsInstance(self.catalog.products, list)
        self.assertGreater(len(self.catalog.products), 0)
    
    def test_get_all_products(self):
        """Test getting all products"""
        products = self.catalog.get_all_products()
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)
    
    def test_search_products(self):
        """Test product search functionality"""
        # Search by name
        results = self.catalog.search_products("headphones")
        self.assertIsInstance(results, list)
        
        # Search by category
        results = self.catalog.search_products("electronics")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_get_product_by_id(self):
        """Test getting product by ID"""
        # Get first product ID
        first_product = self.catalog.products[0]
        
        # Search for it
        product = self.catalog.get_product_by_id(first_product.id)
        self.assertIsNotNone(product)
        self.assertEqual(product.id, first_product.id)
        
        # Test with non-existent ID
        product = self.catalog.get_product_by_id("NONEXISTENT")
        self.assertIsNone(product)
    
    def test_get_products_by_category(self):
        """Test getting products by category"""
        # Get available categories
        categories = self.catalog.get_all_categories()
        
        if categories:
            category = categories[0]
            products = self.catalog.get_products_by_category(category)
            
            self.assertIsInstance(products, list)
            for product in products:
                self.assertEqual(product.category.lower(), category.lower())
    
    def test_get_all_categories(self):
        """Test getting all categories"""
        categories = self.catalog.get_all_categories()
        
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        
        # Check categories are unique
        self.assertEqual(len(categories), len(set(categories)))
    
    def test_search_returns_relevant_results(self):
        """Test search returns relevant results"""
        results = self.catalog.search_products("watch")
        
        for product in results:
            # Check if search term appears in name, category, or description
            search_term_found = (
                "watch" in product.name.lower() or
                "watch" in product.category.lower() or
                "watch" in product.description.lower()
            )
            self.assertTrue(search_term_found)


if __name__ == '__main__':
    unittest.main()
