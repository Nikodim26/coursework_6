from django import template

from config.settings import MEDIA_URL

register = template.Library()

@register.filter()
def media_filter(path):
    if path:
        return f"{MEDIA_URL}{path}"
    return "#"