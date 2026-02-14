"""
Product Catalog Manager
Manages product information and search functionality
"""

import json
from typing import List, Dict, Optional
import os


class Product:
    """Product data model"""
    
    def __init__(self, id: str, name: str, category: str, price: float, 
                 description: str, stock: int, image_url: str = ""):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
    
    def to_dict(self) -> Dict:
        """Convert product to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "stock": self.stock,
            "image_url": self.image_url
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create product from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            description=data["description"],
            stock=data["stock"],
            image_url=data.get("image_url", "")
        )


class ProductCatalog:
    """Manages product catalog and search functionality"""
    
    def __init__(self, catalog_file: Optional[str] = None):
        """Initialize product catalog"""
        self.products: List[Product] = []
        self.catalog_file = catalog_file
        
        if catalog_file and os.path.exists(catalog_file):
            self.load_catalog(catalog_file)
        else:
            self._load_sample_products()
    
    def _load_sample_products(self):
        """Load sample products for demonstration"""
        sample_products = [
            {
                "id": "PROD001",
                "name": "Wireless Bluetooth Headphones",
                "category": "Electronics",
                "price": 79.99,
                "description": "Premium wireless headphones with noise cancellation",
                "stock": 50,
                "image_url": "/static/images/headphones.jpg"
            },
            {
                "id": "PROD002",
                "name": "Smart Fitness Watch",
                "category": "Electronics",
                "price": 199.99,
                "description": "Track your fitness goals with this smart watch",
                "stock": 30,
                "image_url": "/static/images/watch.jpg"
            },
            {
                "id": "PROD003",
                "name": "Classic Cotton T-Shirt",
                "category": "Clothing",
                "price": 24.99,
                "description": "Comfortable 100% cotton t-shirt in various colors",
                "stock": 100,
                "image_url": "/static/images/tshirt.jpg"
            },
            {
                "id": "PROD004",
                "name": "Running Shoes",
                "category": "Footwear",
                "price": 89.99,
                "description": "Lightweight running shoes for optimal performance",
                "stock": 45,
                "image_url": "/static/images/shoes.jpg"
            },
            {
                "id": "PROD005",
                "name": "Leather Wallet",
                "category": "Accessories",
                "price": 34.99,
                "description": "Genuine leather wallet with multiple card slots",
                "stock": 60,
                "image_url": "/static/images/wallet.jpg"
            },
            {
                "id": "PROD006",
                "name": "Laptop Backpack",
                "category": "Accessories",
                "price": 49.99,
                "description": "Durable backpack with padded laptop compartment",
                "stock": 40,
                "image_url": "/static/images/backpack.jpg"
            },
            {
                "id": "PROD007",
                "name": "Smartphone Stand",
                "category": "Electronics",
                "price": 15.99,
                "description": "Adjustable smartphone stand for desk",
                "stock": 80,
                "image_url": "/static/images/stand.jpg"
            },
            {
                "id": "PROD008",
                "name": "Sunglasses",
                "category": "Accessories",
                "price": 59.99,
                "description": "UV protection sunglasses with polarized lenses",
                "stock": 55,
                "image_url": "/static/images/sunglasses.jpg"
            }
        ]
        
        for product_data in sample_products:
            self.products.append(Product.from_dict(product_data))
    
    def load_catalog(self, file_path: str):
        """Load product catalog from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data]
        except Exception as e:
            print(f"Error loading catalog: {e}")
            self._load_sample_products()
    
    def save_catalog(self, file_path: str):
        """Save product catalog to JSON file"""
        with open(file_path, 'w') as f:
            data = [p.to_dict() for p in self.products]
            json.dump(data, f, indent=2)
    
    def search_products(self, query: str) -> List[Product]:
        """
        Search products by name, category, or description
        
        Args:
            query: Search query string
            
        Returns:
            List of matching products
        """
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            if (query_lower in product.name.lower() or
                query_lower in product.category.lower() or
                query_lower in product.description.lower()):
                results.append(product)
        
        return results
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a category"""
        return [p for p in self.products if p.category.lower() == category.lower()]
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.products
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        categories = set(p.category for p in self.products)
        return sorted(list(categories))
