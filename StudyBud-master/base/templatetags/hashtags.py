from django import template
import re

register = template.Library()

@register.filter
def highlight_hashtags(text):
    return re.sub(r"(#\w+)", r'<span class="hashtag">\1</span>', text)
