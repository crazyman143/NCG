from django.db import models
from django.contrib.auth.models import User 	# used in Order

# Cemex Models:

class Item(models.Model):
	number = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=50, blank=False)
	description	= models.TextField(blank=False)
	image = models.FileField(upload_to='item_images/', blank=True)

	def __str__(self):
		if self.number:
			return self.number + ' ' + self.name
		else:
			return self.name


class Attribute(models.Model):
	name = models.CharField(max_length=30, blank=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		parent_item  = Item.objects.get(id = self.item.id)
		return  ('id ' 
				+ str(self.id) 
				+ ' ' + self.name 
				+ ' (' + parent_item.name 
				+ ')'
				)


class Option(models.Model):
	name = models.CharField(max_length=30, blank=False)
	attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

	def __str__(self):
		parent_attribute  = Attribute.objects.get(id = self.attribute.id)
		parent_item = Item.objects.get(id = parent_attribute.item.id)
		return (self.name 
				+ ' (' 
				+ parent_attribute.name 
				+ ') (' 
				+ parent_item.name 
				+ ')'
				)


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField(auto_now=True)
	complete = models.BooleanField(blank=False)
	shipped = models.BooleanField(blank=False)

	def __str__(self):
		return ('id: ' 
				+ str(self.id) 
				+ ' (' + self.user.username 
				+ ')'
				)


class Order_Item(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	item =	models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity =	models.IntegerField(blank=False)

	def __str__(self):
		return ('id: ' 
				+ str(self.id) 
				+ ' Order id ' 
				+ str(self.order.id)
				)
	

class Order_Address(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	email = models.CharField(max_length=30, blank=True)
	address1 = models.CharField(max_length=30, blank=False)
	address2 = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=30, blank=False)
	state = models.CharField(max_length=30, blank=False)
	zip = models.CharField(max_length=30, blank=False)
	phone = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return ('for order: ' 
				+ str(self.order.id) 
				)


class Order_Item_Detail(models.Model):
	attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
	option = models.ForeignKey(Option, on_delete=models.CASCADE)
	order_item = models.ForeignKey(Order_Item, on_delete=models.CASCADE)

	def __str__(self):
		return ('id: ' 
				+ str(self.id) 
				+ ' ordr_itm: ' 
				+ str(self.order_item.id) 
				+ ' ordr id: ' 
				+ str(self.order_item.order.id)
				)