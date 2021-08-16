from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from bot.models import Order

import json

@csrf_exempt
def index(request):
	try:
		data = json.loads(request.POST['data'])
		order = Order()

		order.order = json.dumps(data['order'])
		order.price = 92813
		order.date = timezone.now()
		order.customer_name = data['cname']
		order.customer_phone = data['phone']
		# order.customer_location = data['location']
		order.customer_username = data['username']
		order.customer_id = int(data['id'])
		order.source = 'robot'
		order.save()

		return HttpResponse('Got')
	except Exception as e:
		print(e)
		return HttpResponse(e)