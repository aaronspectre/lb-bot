from django.urls import path
from interface import views


urlpatterns = [
	path('', views.auth, name = 'auth'),
	path('sign-in', views.signIn, name = 'signIn'),
	path('dashboard/<str:status>', views.dashboard, name = 'dashboard'),
	path('order-validation/<int:id>', views.orderValidation, name = 'orderValidation'),
	path('add', views.addOrder, name = 'add'),
	path('add/handle', views.addOrderHandle, name = 'add_handle'),
]