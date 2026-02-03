# member's and company related articles data
class Article:
    def __init__(
        self,
        headline,
        article_short,
        article_start,
        article_end,
        article_image,
        article_link,
        author,
    ):
        self.headline = headline
        self.article_short = article_short
        self.article_start = article_start
        self.article_end = article_end
        self.article_image = article_image
        self.article_link = article_link
        self.author = author
        
    # for debuuging
    def __repr__(self):
        return f"Article(headline={self.headline!r})"
    
    # quick output
    def __str__(self):
        return f"{self.headline} ({self.article_start} to {self.article_end})"
    
    def to_dict(self):
        return {
            'headline': self.headline,
            'article_short': self.article_short,
            'article_start': self.article_start,
            'article_end': self.article_end,
            'article_image': self.article_image,
            'article_link': self.article_link,
            'author': self.author
        }