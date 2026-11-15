from django import template
from config.settings import MEDIA_URL

register = template.Library()

@register.filter()
def media_filter(path):
    if path:
        return f"{MEDIA_URL}{path}"
    return "#"

# @register.filter
# def path_in(path, paths_str):
#     path = path.split('/')[1]
#     paths_str=paths_str.replace('/','')
#     paths = [p.strip() for p in paths_str.split(',') if p.strip()]
#
#     return path in paths

@register.filter
def email_local_part(email):
    if not email:
        return ""
    parts = email.split("@", 1)
    return parts[0] if len(parts) > 1 else email







