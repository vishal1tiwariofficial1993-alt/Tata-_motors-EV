"""
Vercel serverless function handler
Maps requests to Flask app
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app

# Vercel serverless handler
def handler(request):
    """Handle incoming requests for Vercel"""
    with app.test_request_context(
        path=request.path,
        method=request.method,
        headers=dict(request.headers),
        data=request.get_data()
    ):
        return app.full_dispatch_request()
