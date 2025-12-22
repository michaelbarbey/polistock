from app.api import app
import os

if __name__ == "__main__":
    print("Starting Polistock API...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

# For production - CRITICAL: EB looks for 'application'
application = app
