from django.db import models
from account.models import Profile
from .models import *
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=100, null = False, blank=False)
	picture = models.ImageField(upload_to='images')

	def __str__(self):
		return self.name

class City(models.Model):
	name = models.CharField(max_length = 100, null = False, blank=False)
	latitude = models.FloatField()
	longitude = models.FloatField()
	date_cr = models.DateTimeField(auto_now_add = True)

	class Meta:
		ordering=('date_cr',)

	def __str__(self):
		return self.name

class Currency(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	
	def __str__(self):
		return self.name


class Product(models.Model):
	seller = models.ForeignKey(Profile, on_delete = models.SET_NULL, null =True)
	title = models.CharField(max_length = 155, null = False, blank = False)
	category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
	description = models.TextField()
	price = models.IntegerField()
	money_type = models.ForeignKey(Currency, on_delete = models.SET_NULL, null = True)
	localization = models.ForeignKey(City, on_delete = models.SET_NULL, null= True)
	principal_img = models.ForeignKey('Product_Image', on_delete = models.CASCADE, null = True)
	date_posted = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f'{self.id}'


def product_default_image():
	return f"images/product_pictures/default.jpg"


class Product_Image(models.Model):
	product_name = models.ForeignKey(Product, on_delete = models.CASCADE)
	image = models.ImageField(upload_to='images')
	
	def __str__(self):
 		return f'{self.product_name.id}'


class Favourite(models.Model):
	user = models.OneToOneField(Profile, on_delete = models.SET_NULL, null=True)
	products = models.ManyToManyField(Product)

	def __str__(self):
		return str(self.id)


class ChatRoomName(models.Model):
	name = models.CharField(max_length= 255)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Message(models.Model):
	user_id = models.CharField(max_length = 255)
	room = models.ForeignKey(ChatRoomName, on_delete=models.CASCADE,null=True,max_length = 255)
	content = models.TextField()
	data_added = models.DateTimeField(auto_now_add= True)

	class Meta:
		ordering = ('data_added', )

	def __str__(self):
		return str(self.id)