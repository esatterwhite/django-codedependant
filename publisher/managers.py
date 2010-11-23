from django.db.models import Manager
CURRENT_ARTICLES = 5
LIVE_ARTICLES = [5,6]
ARCHIVE = 6
class LiveArticleManager(Manager):
    # The Article Manager ensures that only LIVE STORIES are returned
    # to view functions and page templates
    
    def get_query_set(self):
        default_query_set= super(LiveArticleManager,self).get_query_set()
        
        # This excludes any 'Game Summaries' Assuming they are the first categoy in the list :(
        return default_query_set.filter(status__in = LIVE_ARTICLES)
class CurrentArticleManager(Manager):
    def get_query_set(self):
        default_query_set = super(CurrentArticleManager, self).get_query_set()
        return default_query_set.filter(status = CURRENT_ARTICLES)
class ArchivedArticleManager(Manager):
    def get_query_set(self):
        default_query_set = super(ArchivedArticleManager,self).get_query_set() 
        return default_query_set.filter(status = ARCHIVE)