from flask import Flask, request, jsonify
from flask_cors import CORS
from services.google_civic_service import GoogleCivicDistrictValue
from services.congress_service import CongressMemberProfile
from services.capitol_trades_service import CapitolTrades
from services.news_service import NewsArticles
from app.polistock_app import get_official_by_address

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:3000",
            "https://d2nwhjh2rxmyof.cloudfront.net",
            "https://polistock.cis4160.com",
            "http://polistock.cis4160.com",
            "https://polidemos.com",           
            "https://www.polidemos.com",       
            "http://polidemos.com",            
            "http://localhost:5173"            
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "polistock-api"
    }), 200

@app.route('/api/official', methods=['OPTIONS'])
def options_official():
    """Handle preflight OPTIONS request"""
    response = app.make_default_options_response()
    return response

@app.route('/api/official', methods=['OPTIONS', 'POST'])
def get_official():
    # Handle OPTIONS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    # Handle POST request
    try:
        print("\n=== API Request received ===")
        data = request.get_json()
        print(f"Request data: {data}")
        
        result = get_official_by_address(data)
        
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result is dict: {isinstance(result, dict)}")
        if result:
            print(f"DEBUG: Result keys: {result.keys() if isinstance(result, dict) else 'NOT A DICT'}")
            
            # Check each field
            for key, value in result.items():
                try:
                    import json
                    json.dumps({key: value})
                    print(f"  ✓ {key}: OK")
                except Exception as e:
                    print(f"  ✗ {key}: FAILED - {type(value)} - {e}")
            
            # MAKE SURE THIS RETURN IS HERE:
            return jsonify({'official': result}), 200
        else:
            return jsonify({'error': 'Failed to fetch official data'}), 404
            
    except Exception as e:
        print(f"ERROR in get_official endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/official/<bioguide_id>', methods=['GET'])
def get_official_by_id(bioguide_id):
    """
    gets official data by bioguide ID
    example: GET /api/official/G000583
    """
    try:
        
        # fetches the official directly by bioguide_id
        return jsonify({
            "message": "Endpoint not implemented yet",
            "bioguide_id": bioguide_id
        }), 501
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
        
@app.route('/api/transactions/<bioguide_id>', methods=['GET'])
def get_transactions(bioguide_id):
    """
    gets only transactions for an official
    
    query params:
    - limit: number of transactions (default: 25)
    """
    try:
        limit = request.args.get('limit', 25, type=int)
        
        return jsonify({
            "message": "Endpoint not implemented yet",
            "bioguide_id": bioguide_id,
            "limit": limit
        }), 501
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
        
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

application = app
