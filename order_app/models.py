from django.db import models
from auth_app.models import *
from product_app.models import *
from django.core.validators import MinValueValidator
from django.utils.timezone import now

class WishList(models.Model):
	customer 			= models.ForeignKey(Account, on_delete=models.CASCADE)
	product 		    = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
class CartItem(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.pk)
	
class Address(models.Model):
    customer			= models.ForeignKey(Account, on_delete=models.CASCADE)
    title               = models.CharField(max_length=50, default='Title')
    name                = models.CharField(max_length=50)
    email               = models.EmailField(max_length=60)
    line_1              = models.CharField(max_length=50)

    def __str__(self):
        return self.name
	
	
class Order(models.Model):
    customer                    = models.ForeignKey(Account, on_delete=models.CASCADE)
    address                     = models.ForeignKey(Address, on_delete=models.CASCADE)
    product                     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity                    = models.PositiveIntegerField(default=1)
    payment                     = models.CharField(max_length=50)
    date                        = models.DateTimeField(default=now)
    status                      = models.CharField(max_length=50)
    admin_action                = models.BooleanField(default=True)
    net_total                   = models.PositiveIntegerField(default=0)
    razorpay_paid               = models.BooleanField(default=False, null=True, blank=True)
    razorpay_order_id           = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id         = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature  = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    
class RazorpayDemo(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)