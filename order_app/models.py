from django.db import models
from auth_app.models import *
from product_app.models import *

class WishList(models.Model):
	customer 			= models.ForeignKey(Account, on_delete=models.CASCADE)
	product 		    = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
class Cart(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.CharField(max_length=60, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.pk)
	
class Address(models.Model):
	customer			= models.ForeignKey(Account, on_delete=models.CASCADE)
	name                = models.CharField(max_length=50)
	email               = models.EmailField(max_length=60)
	line_1              = models.CharField(max_length=50)

	def __str__(self):
		return self.name
	
	
class Order(models.Model):
	customer			= models.ForeignKey(Account, on_delete=models.CASCADE)
	address             = models.ForeignKey(Address, on_delete=models.CASCADE)
	cart_item           = models.ForeignKey(Product, on_delete=models.CASCADE)
	payment             = models.CharField(max_length=50)
	date                = models.CharField(max_length=50)
	status              = models.CharField(max_length=50)
	admin_action        = models.BooleanField(default=True)

	def __str__(self):
		return self.name