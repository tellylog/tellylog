import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
register = template.Library()


@register.filter(name='access')
def access(value, arg):
    return value[arg]


@register.filter
def joinby(value, arg):
    return arg.join(value)


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.simple_tag
def smart_limit(content, length=240, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


@register.simple_tag
def fill_rating(current, rating):
    if rating is 0:
        return 'fa-star-o'
    if current < rating:
        return 'fa-star rating__btn--active'
    else:
        return 'fa-star-o'
