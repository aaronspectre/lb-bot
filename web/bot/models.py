from django.db import models




class Order(models.Model):
	customer = models.CharField(max_length = 100)
	customer_id = models.IntegerField()
	customer_username = models.CharField(max_length = 100)
	customer_phone = models.CharField(max_length = 30)
	customer_location = models.CharField(max_length = 40)
	customer_name = models.CharField(max_length = 100)

	order = models.JSONField(default = list)
	source = models.CharField(max_length = 10, default = 'cash-register')
	price = models.FloatField(max_length = 30)
	status = models.CharField(max_length = 10, default = 'pending')
	ready_status = models.CharField(max_length = 10, default = 'sold')
	date = models.DateTimeField()

	def __str__(self):
		return self.customer_name