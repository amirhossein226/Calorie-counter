from django import template

register = template.Library()


@register.filter
def truncate(content, length):
    return content[:length] + "..."
