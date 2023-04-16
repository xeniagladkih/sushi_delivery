from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=10, blank=True) 

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=6, decimal_places=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='item')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        ordermodels = self.ordermodel_set.all()
        total = sum([item.get_total for item in ordermodels])
        return total 

    @property
    def get_cart_items(self):
        ordermodels = self.ordermodel_set.all()
        total = sum([item.quantity for item in ordermodels])
        return total 
    

class OrderModel(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
         total = self.menu_item.price * self.quantity
         return total
    
class ShippingAddress(models.Model):
	customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address