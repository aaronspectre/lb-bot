from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from bot.models import Order

import json

def auth(request):
	return render(request, 'auth.html')


def signIn(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username = username, password = password)

	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))

	else:
		return HttpResponseRedirect(reverse('auth'))



@login_required
def dashboard(request, status):
	orders = Order.objects.filter(status = status)
	return render(request, 'dashboard.html', {'orders': orders})


@login_required
def orderValidation(request, id):
	order = get_object_or_404(Order, id = id)
	if order.status == 'pending' and order.source == 'robot':
		order.status = 'delivery'
	elif order.status == 'pending' and order.source == 'cash-register':
		order.status = 'done'
		order.source = 'check-square'
	elif order.status == 'delivery':
		order.status = 'done'
		order.source = 'check-square'

	order.save()
	return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))


@login_required
def addOrder(request):
	return render(request, 'add-order.html')


@login_required
def addOrderHandle(request):
	order = Order()

	order.order = request.POST['order'].split('|')
	order.order.pop()
	order.order = json.dumps(order.order)

	order.price = request.POST['price']
	order.date = timezone.now()
	order.customer_name = request.POST['cname']
	order.customer_phone = request.POST['cphone']

	order.save()

	if len(order.customer_name) == 0:
		order.customer_name = f'Customer {order.id}'
		order.save()


	return HttpResponseRedirect(reverse('dashboard', args = ('pending',)))