from newspaper import Article

def getHeadline():
    article = Article(url)
    article.download()
    article.parse()
    return article.title