import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.app import app

# Vercel requires the app to be available at the module level
# This is the WSGI application Vercel will use
app = app

if __name__ == "__main__":
    app.run()
