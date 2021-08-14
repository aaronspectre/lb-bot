import json
from django import template


register = template.Library()


@register.filter
def parser(item):
	return json.loads(item)