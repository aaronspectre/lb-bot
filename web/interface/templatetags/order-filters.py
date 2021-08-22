import json
from django import template


register = template.Library()


@register.filter
def parser(item):
	try:
		return json.loads(item)
	except Exception as e:
		pass


# https://maps.googleapis.com/maps/api/geocode/json?latlng={{40.714224}},{{-73.961452}}&location_type=ROOFTOP&result_type=street_address&key=

@register.filter
def getLocation(location, direction):
	try:
		location = json.loads(location)
		if direction == '1':
			return location['latitude']
		else:
			return location['longitude']
	except Exception as e:
		print(e)


@register.filter
def summ(orders):
	total = 0
	for order in orders:
		if order.status == 'done':
			total+=order.price

	return total

