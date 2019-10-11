# https://stackoverflow.com/questions/4651172/reference-list-item-by-index-within-django-template

from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]
