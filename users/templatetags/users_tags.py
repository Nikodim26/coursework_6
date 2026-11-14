from django import template
from django.contrib.auth.models import Group

from config.settings import MEDIA_URL
from django.conf import settings

register = template.Library()

@register.filter()
def media_filter(path):
    if path:
        return f"{MEDIA_URL}{path}"
    return "#"

@register.filter
def path_in(path, paths_str):
    paths = [p.strip() for p in paths_str.split(',') if p.strip()]
    return path in paths

@register.filter
def email_local_part(email):
    if not email:
        return ""
    parts = email.split("@", 1)
    return parts[0] if len(parts) > 1 else email







