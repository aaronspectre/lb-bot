from django.urls import path

from bot import views



urlpatterns = [
	path('', views.index, name = 'index'),
	# path('/new_order', views.new_order, name = 'new_order'),
]