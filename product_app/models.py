from django.db import models

# Create your models here.
class Category(models.Model):
	name 				= models.CharField(max_length=50)
	description 		= models.TextField()
	image 				= models.ImageField(upload_to='categories')

	def __str__(self):
		return self.name

class Subcategory(models.Model):
	name 				= models.CharField(max_length=50)
	category			= models.ForeignKey(Category, on_delete=models.CASCADE)
	description 		= models.TextField()
	image 				= models.ImageField(upload_to='sub_categories')

	def __str__(self):
		return self.name

class Brand(models.Model):
	name 				= models.CharField(max_length=50)
	description 		= models.TextField()
	image 				= models.ImageField(upload_to='brands')

	def __str__(self):
		return self.name

class Product(models.Model):
	name 				= models.CharField(max_length=50)
	brand				= models.ForeignKey(Brand, on_delete=models.CASCADE)
	description 		= models.CharField(max_length=100)
	category	 		= models.ForeignKey(Category, on_delete=models.CASCADE)
	sub_category	 	= models.ForeignKey(Subcategory, on_delete=models.CASCADE)
	mrp 				= models.CharField(max_length=50)
	image 				= models.ImageField(upload_to='products')
	availability 		= models.BooleanField(default=False)
	stock 				= models.CharField(max_length=50)
	sell_count			= models.CharField(max_length=10, default='0')
	date_added			= models.DateTimeField(auto_now_add=True,)


	def __str__(self):
		return self.name
	
class Names(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name