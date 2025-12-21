# article time
import requests
import json
from datetime import datetime
from models.article import Article
#from utils.date_helpers import format_date
from config.settings import NYT_API_KEY, NYT_API_URL, DEFAULT_NEWS_LIMIT

class NewsArticles(Article):
    
    def __init__(self):
        self.NYT_KEY = NYT_API_KEY
        self.base_url =NYT_API_URL        
    
    def execute(self, article_begin_date, article_end_date, filter_query, query):

        # formatting dates from capitoltrades
        from_datestr = article_begin_date

        # parsing dates
        date_from = datetime.strptime(from_datestr, "%d %b %Y")

        # format to YYYYMMDD
        from_date = date_from.strftime("%Y%m%d")
        
        # repeating with respective date
        to_datestr = article_end_date

        # parse to
        date_to = datetime.strptime(to_datestr, "%d %b %Y")

        # format to YYYYMMDD
        to_date = date_to.strftime("%Y%m%d")
        
        nyt_endpoint = f"{from_date}&end_date={to_date}&fq={filter_query}&q={query}&sort=relevance&api-key={self.NYT_KEY}"
        
        nyt_request_url = f"{self.base_url}{nyt_endpoint}"
        requestHeaders = {
            "Accept": "application/json"
        }
        
        # params = {
        #     "api-key": self.api_key,
        #     "begin_date": begin_date,
        #     "end_date": end_date,
        #     "fq": filter_query,
        #     "q": query
        # }
        
        # nyt_response = requests.get(nyt_request_url, params=params)
        nyt_response = requests.get(nyt_request_url, headers=requestHeaders)
        nyt_response.status_code
        if nyt_response.status_code == 200:
            nyt_results = nyt_response.json()
            nyt_results = json.dumps(nyt_results, indent=4)
            return nyt_results
        
    def to_parse(self, nyt_results):
        
        nyt_to_parse = nyt_results
        to_parse = json.loads(nyt_to_parse) # type: ignore
        articles = DEFAULT_NEWS_LIMIT
        
        news_components = []
        for article in range(articles):
            #display(Image(url=to_parse["response"]["docs"][article]["multimedia"]["default"]["url"]))
            headline = to_parse["response"]["docs"][article]["headline"]["main"]
            image_url = to_parse["response"]["docs"][article]["multimedia"]["default"]["url"]
            print(f"{headline}"
                  f"{image_url}")
            news_components.append(headline)
            news_components.append(image_url)
        return news_components
    
    def article_endpoints(self,headline, article_begin_date, article_end_date, filter_query, query, image_url):
        endpoints = Article(
            headline=headline,
            article_start=article_begin_date,
            article_end=article_end_date,
            filter_query=filter_query,
            query=query,
            article_short=None,
            article_image=image_url,
        )
        # print(endpoints)
        return endpoints