from app.api import app

if __name__ == "__main__":
    print("Starting Polistock API...")
    print("API will be available at http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  - GET  /api/health")
    print("  - POST /api/official")
    print("  - GET  /api/official/<bioguide_id>")
    print("  - GET  /api/transactions/<bioguide_id>")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
