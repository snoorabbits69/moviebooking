from django import template
from ..models import Show
register=template.Library()

@register.simple_tag
def movie_price(id):
    return Show.objects.filter(movie=id)