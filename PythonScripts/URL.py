from newspaper import Article

def getHeadline(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title