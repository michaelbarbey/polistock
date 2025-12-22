# article time
import requests
import json
from utils.date_helpers import format_date
from models.article import Article
#from utils.date_helpers import format_date
from config.settings import NYT_API_KEY, NYT_API_URL, DEFAULT_NEWS_LIMIT

# class NewsArticles(Article):
    
#     def __init__(self):
#         self.NYT_KEY = NYT_API_KEY
#         self.base_url =NYT_API_URL        
    
#     def execute(self, article_begin_date, article_end_date, filter_query, query):

#         # formatting dates from capitoltrades
#         from_datestr = article_begin_date

#         # parsing dates
#         date_from = datetime.strptime(from_datestr, "%d %b %Y")

#         # format to YYYYMMDD
#         from_date = date_from.strftime("%Y%m%d")
        
#         # repeating with respective date
#         to_datestr = article_end_date

#         # parse to
#         date_to = datetime.strptime(to_datestr, "%d %b %Y")

#         # format to YYYYMMDD
#         to_date = date_to.strftime("%Y%m%d")
        
#         nyt_endpoint = f"{from_date}&end_date={to_date}&fq={filter_query}&q={query}&sort=relevance&api-key={self.NYT_KEY}"
        
#         nyt_request_url = f"{self.base_url}{nyt_endpoint}"
#         requestHeaders = {
#             "Accept": "application/json"
#         }
        
#         # params = {
#         #     "api-key": self.api_key,
#         #     "begin_date": begin_date,
#         #     "end_date": end_date,
#         #     "fq": filter_query,
#         #     "q": query
#         # }
        
#         # nyt_response = requests.get(nyt_request_url, params=params)
#         nyt_response = requests.get(nyt_request_url, headers=requestHeaders)
#         nyt_response.status_code
#         if nyt_response.status_code == 200:
#             nyt_results = nyt_response.json()
#             nyt_results = json.dumps(nyt_results, indent=4)
#             return nyt_results
        
#     def to_parse(self, nyt_results):
#         # nyt_to_parse = nyt_results
#         # to_parse = json.loads(nyt_to_parse) # type: ignore
#         # articles = DEFAULT_NEWS_LIMIT
        
#         # news_components = []
#         # for article in range(articles):
#         #     #display(Image(url=to_parse["response"]["docs"][article]["multimedia"]["default"]["url"]))
#         #     headline = to_parse["response"]["docs"][article]["headline"]["main"]
#         #     image_url = to_parse["response"]["docs"][article]["multimedia"]["default"]["url"]
#         #     print(f"{headline}"
#         #           f"{image_url}")
#         #     news_components.append(headline)
#         #     news_components.append(image_url)
#         # return news_components
    
#     def article_endpoints(self,headline, article_begin_date, article_end_date, filter_query, query, image_url):
#         endpoints = Article(
#             headline=headline,
#             article_start=article_begin_date,
#             article_end=article_end_date,
#             filter_query=filter_query,
#             query=query,
#             article_short=None,
#             article_image=image_url,
#         )
#         # print(endpoints)
#         return endpoints

class NewsArticles:
    def __init__(self):
        self.api_key = NYT_API_KEY
        self.base_url = NYT_API_URL
    
    def execute(self, article_begin_date, article_end_date, filter_query, query):
        """
        Execute NYT API search.
        
        Returns:
            dict: API response with articles
        """
        try:
            # Format dates
            begin_date = format_date(article_begin_date)
            end_date = format_date(article_end_date)
            
            params = {
                "api-key": self.api_key,
                "begin_date": begin_date,
                "end_date": end_date,
                "fq": filter_query,
                "q": query
            }
            
            print(f"Calling NYT API with query: {query}")
            print(f"Date range: {begin_date} to {end_date}")
            
            response = requests.get(self.base_url, params=params)
            
            print(f"NYT API status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"NYT API Error: {response.text}")
                return None
            
            data = response.json()
            print(f"NYT API returned {data.get('response', {}).get('meta', {}).get('hits', 0)} results")
            
            return data
            
        except Exception as e:
            print(f"Error calling NYT API: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def to_parse(self, results):
        """
        Parse top articles from results.
        Returns:
        list: List of (headline, image_url) tuples
        """
        articles = []
    
        # Add safety checks
        if not results:
            print("No results to parse")
            return articles
        
        response = results.get("response")
        if not response:
            print("No 'response' key in results")
            return articles
        
        docs = response.get("docs", [])
        
        # Add check for None
        if docs is None:
            docs = []
        
        print(f"Parsing {len(docs)} documents")
        
        # Limit to DEFAULT_NEWS_LIMIT articles
        for doc in docs[:DEFAULT_NEWS_LIMIT]:
            try:
                headline = doc.get("headline", {}).get("main", "No headline")
                
                # Get image URL - handle case where multimedia might be empty
                multimedia = doc.get("multimedia", [])
                image_url = ""
                if multimedia and len(multimedia) > 0:
                    image_url = f"https://www.nytimes.com/{multimedia[0].get('url', '')}"
                
                articles.append((headline, image_url))
                print(f"Parsed article: {headline[:50]}...")
                
            except Exception as e:
                print(f"Error parsing individual article: {e}")
                continue
        
        print(f"Successfully parsed {len(articles)} articles")
        return articles
    
    def article_endpoint(self, headline, article_begin_date, article_end_date, 
                        filter_query, query, image_url):
        """
        Create Article object from endpoint data.
        
        Returns:
            Article: Article object with data
        """
        article = Article(
            headline=headline,
            article_start=article_begin_date,
            article_end=article_end_date,
            filter_query=filter_query,
            query=query,
            article_short=headline[:100] if headline else "",  # Short snippet
            article_image=image_url
        )
        
        return article
    
    