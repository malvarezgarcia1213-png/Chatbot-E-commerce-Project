from setuptools import setup, find_packages

setup(
    name="ecommerce-chatbot",
    version="1.0.0",
    description="An intelligent chatbot for E-commerce to increase sales and customer satisfaction",
    author="E-commerce Chatbot Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "flask-socketio>=5.3.5",
        "python-socketio>=5.10.0",
        "nltk>=3.9",
        "scikit-learn>=1.3.2",
        "numpy>=1.26.2",
        "pandas>=2.1.4",
    ],
    python_requires=">=3.8",
)
