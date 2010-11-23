'''
Created on Nov 23, 2010

@author: Eric Satterwhite
'''

from django.dispatch import Signal

article_was_published = Signal(providing_args=['article'])
article_was_edited =    Signal(providing_args=['article'])