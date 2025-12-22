
from app.api import app
import os

if __name__ == "__main__":
    # Local development
    print("Starting Polistock API...")
    print("API will be available at http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  - GET  /api/health")
    print("  - POST /api/official")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

application = app