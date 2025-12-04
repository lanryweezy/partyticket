"""
WSGI entry point for production deployment.
"""
from app import create_app
import os

# Create application instance
app = create_app(os.environ.get('FLASK_CONFIG', 'production'))

if __name__ == "__main__":
    app.run()


