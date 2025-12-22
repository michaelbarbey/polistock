# member's and company related articles data
class Article:
    def __init__(
        self,
        headline,
        article_start,
        article_end,
        filter_query,
        query,
        article_short,
        article_image,
    ):
        self.headline = headline
        self.article_start = article_start
        self.article_end = article_end
        self.filter_query = filter_query
        self.query = query
        self.article_short = article_short
        self.article_image = article_image
        
    # for debuuging
    def __repr__(self):
        return f"Article(headline={self.headline!r})"
    
    # quick output
    def __str__(self):
        return f"{self.headline} ({self.article_start} to {self.article_end})"