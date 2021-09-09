from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from bot.models import Order

import json

@csrf_exempt
def index(request):
	try:
		print(request.POST)
		data = json.loads(request.POST['data'])
		order = Order()

		order.order = json.dumps(data['order'])
		order.date = timezone.now()
		order.customer_name = data['cname']
		order.customer_phone = data['phone']
		order.customer_location = json.dumps(data['location'])
		order.customer_username = data['username']
		order.customer_id = int(data['id'])
		order.price = order.customer_id * 8
		order.source = 'robot'
		order.save()

		return HttpResponse('Got')
	except Exception as e:
		print(e)
		return HttpResponse(e)