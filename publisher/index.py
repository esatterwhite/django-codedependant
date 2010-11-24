'''
Created on Nov 23, 2010

@author: Eric
'''
from djapian import space, Indexer
from models import Article

class ArticleIndexer(Indexer):
    fields = ['title','content']
    tags = [
        ('title','title', 3),
        ('content', 'as_plain_text', 1)
    ]

space.add_index(Article, ArticleIndexer, attach_as='indexer')