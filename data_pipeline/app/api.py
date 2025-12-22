from flask import Flask, request, jsonify
from flask_cors import CORS
from services.google_civic_service import GoogleCivicDistrictValue
from services.congress_service import CongressMemberProfile
from services.capitol_trades_service import CapitolTrades
from services.news_service import NewsArticles

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",  # Local development
            "http://localhost:3000",  # Alternative local port
            "https://d2nwhjh2rxmyof.cloudfront.net"  # Replace with your actual CloudFront URL
        ]
    }
})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "polistock-api"
    }), 200
    
@app.route('/api/official', methods=['POST'])
def get_official():
    """
    Get official data by address
    
    Request body:
    {
        "street": "121 highwood rd",
        "city": "east williston",
        "state": "new york",
        "zipcode": "11596"
    }
    
    Response:
    {
        "official": {
            "firstname": "...",
            "lastname": "...",
            "fullname": "...",
            "bioguide_id": "...",
            "party": "...",
            "chamber": "...",
            "term_start": "...",
            "term_end": "...",
            "photo_url": "...",
            "districts": [...],
            "transactions": [...],
            "articles": [...]
        }
    }
    """
    
    try:
        # gets request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')
        
        # validates required fields
        if not all([street, city, state, zipcode]):
            return jsonify({
                "error": "Missing required fields",
                "required": ["street", "city", "state", "zipcode"]
            }), 400
        
        # 1. Get district information
        google_civic = GoogleCivicDistrictValue()
        district_profile = google_civic._fetch_ocd_id(street, city, state, zipcode)
        
        if not district_profile:
            return jsonify({"error": "Could not find district information"}), 404
        
        # 2. Get congress member
        congress_member = CongressMemberProfile()
        congress_profile = congress_member.get_congress_member(district_profile)
        
        if not congress_profile:
            return jsonify({"error": "Could not find congress member"}), 404
        
        # 3. Get transaction data
        print("\n3. Scraping Capitol Trades...")
        capitol_activity = CapitolTrades()
        member_profile = capitol_activity.scrape_politician(congress_profile, limit=25)

        # Check if transactions is None and initialize if needed
        if not hasattr(member_profile, 'transactions') or member_profile.transactions is None:
            member_profile.transactions = []
            print("No transactions found or transactions is None")
        else:
            print(f"SUCCESS: Got {len(member_profile.transactions)} transactions")
        
        # 4. Get profile image
        print("\n4. Fetching headshot...")
        profile_with_img = capitol_activity.fetch_headshot_url(member_profile)
        
        # 5. Get news articles (if transactions exist)
        if profile_with_img.transactions and len(profile_with_img.transactions) > 0:
            try:
                print("\n5. Fetching news articles...")
                first_transaction = profile_with_img.transactions[0]
                article_from = first_transaction.traded_date
                article_to = first_transaction.published_date
                company_query = first_transaction.company
                member_query = profile_with_img.fullname
                
                relevant_news = NewsArticles()
                member_news = relevant_news.execute(
                    article_from, article_to, company_query, member_query
                )
                
                if member_news:
                    try:
                        top_stories = relevant_news.to_parse(member_news)
                        
                        if top_stories:
                            for headline, image_url in top_stories:
                                profile_with_img.officials_articles(
                                    headline=headline,
                                    article_start=article_from,
                                    article_end=article_to,
                                    filter_query=company_query,
                                    query=member_query,
                                    article_short=headline[:100] if headline else "",
                                    article_image=image_url
                                )
                            print(f"Added {len(top_stories)} articles to profile")
                        else:
                            print("No articles returned from parser")
                    except Exception as parse_error:
                        print(f"Error parsing articles (non-fatal): {parse_error}")
                else:
                    print("NYT API returned no data")
            
            except Exception as news_error:
                print(f"Error fetching news (non-fatal): {news_error}")
                import traceback
                traceback.print_exc()
        else:
            print("\n5. No transactions available, skipping news articles")

        # 6. Convert to dictionary for JSON response
        print("\n6. Converting to JSON...")
        response_data = profile_with_img.to_dict()

        print("\n=== API call successful ===\n")

        return jsonify({
            "success": True,
            "official": response_data
        }), 200
        # 5. Get news articles (if transactions exist)
        # if profile_with_img.transactions:
        #     first_transaction = profile_with_img.transactions[0]
        #     article_from = first_transaction.traded_date
        #     article_to = first_transaction.published_date
        #     company_query = first_transaction.company
        #     member_query = profile_with_img.fullname
            
        #     relevant_news = NewsArticles()
        #     member_news = relevant_news.execute(
        #         article_from, article_to, company_query, member_query
        #     )
        #     top_stories = relevant_news.to_parse(member_news)
            
        #     # Add articles to profile
        #     for headline, image_url in top_stories:
        #         article = relevant_news.article_endpoint(
        #             headline, article_from, article_to,
        #             company_query, member_query, image_url
        #         )
        #         profile_with_img.officials_articles(article)
        
        # # convert to dictionary for JSON response
        # response_data = profile_with_img.to_dict()
        
        
        # return jsonify({
        #     "success": True,
        #     "official": response_data
        # }), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/official/<bioguide_id>', methods=['GET'])
def get_official_by_id(bioguide_id):
    """
    gets official data by bioguide ID
    example: GET /api/official/G000583
    """
    try:
        # This would need implementation based on your needs
        # You'd fetch the official directly by bioguide_id
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
        
        # This would need the official object first
        # For now, return not implemented
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
    # development server
    app.run(debug=True, host='0.0.0.0', port=5000)