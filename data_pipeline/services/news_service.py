# article time
import requests
from datetime import datetime
from models.article import Article
#from config.settings import NYT_API_KEY, NYT_API_URL
from config.settings import NYT_API_KEY, NYT_API_URL, DEFAULT_NEWS_LIMIT

class NewsArticles:
    def __init__(self):
        self.api_key = NYT_API_KEY
        self.base_url = NYT_API_URL
    
    def format_date_endpoint(self, date_str):
        if not date_str:
            return None
        
        try:
            if len(date_str) == 8 and date_str.isdigit():
                return date_str
            
            if '-' in date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%Y%m%d')
            
            return date_str
        except Exception as e:
            print(f"Error formatting date {date_str}: {e}")
            return None
    
    # get articles from company
    def get_articles(self, company_name, traded_date=None, end_date=None, limit=DEFAULT_NEWS_LIMIT):
        
        try:
            # format dates
            begin_date = self.format_date_endpoint(traded_date) if traded_date else None
            
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            else:
                end_date = self.format_date_endpoint(end_date)
            
            # endpoint parameters
            params = {
                'q': company_name,
                'fq': 'desk:("Business", "Politics")',
                'sort': 'relevance',
                'api-key': self.api_key
            }
            
            if begin_date:
                params['begin_date'] = begin_date
            if end_date:
                params['end_date'] = end_date
            
            print(f"fetching nyt api",
                  f"company name: {company_name},",
                  f"begin date: {begin_date},",
                  f"end date: {end_date}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # parsing article
            articles = []
            docs = data.get('response', {}).get('docs', [])
            print(f"found {len(docs)} articles from NYT API")
            
            # if docs:
            #     print("\n=== DEBUG: First article structure ===")
            #     first_doc = docs[0]
            #     print(f"Keys in document: {first_doc.keys()}")
            #     print(f"Multimedia type: {type(first_doc.get('multimedia'))}")
            #     print(f"Multimedia content: {first_doc.get('multimedia')}")
            #     print("=== END DEBUG ===\n")
                        
            for doc in docs[:limit]:
                try:
                    byline_data = doc.get('byline', {})
                    #article data
                    author = byline_data.get('original', 'Unknown Author') if isinstance(byline_data, dict) else 'Unknown Author'
                    
                    headline_data = doc.get('headline', {})
                    headline = headline_data.get('main', 'No headline') if isinstance(headline_data, dict) else 'No headline'
                    
                    snippet = doc.get('snippet', '')
                    web_url = doc.get('web_url', '')
                    pub_date = doc.get('pub_date', '')
                    
                    # article image
                    article_image = None
                    multimedia = doc.get('multimedia', {})
                    
                    if isinstance(multimedia, dict):
                        default_img = multimedia.get('default', {})
                        if isinstance(default_img, dict) and 'url' in default_img:
                            article_image = default_img['url']
                        elif multimedia.get('thumbnail', {}).get('url'):
                            article_image = multimedia['thumbnail']['url']
                    
                    elif isinstance(multimedia, list):
                        for media in multimedia:
                            if isinstance(media, dict):
                                url = media.get('url') or media.get('legacy', {}).get('xlarge')
                                if url:
                                    if url.startswith('http'):
                                        article_image = url
                                    else:
                                        article_image = f"https://static01.nyt.com/{url}"
                                    break
                    print(f"  Article: {headline[:50]}...")
                    print(f"  Image: {article_image if article_image else 'No image'}")
                    
                    # article object
                    article = Article(
                        headline=headline,
                        article_short=snippet,
                        article_start=pub_date[:10] if pub_date else None,
                        article_end= end_date,
                        article_image=article_image,
                        article_link=web_url,
                        author=author,
                    )
                    articles.append(article)
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            return articles
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NYT articles: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in NYT service: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    