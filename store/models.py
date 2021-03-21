from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer (models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Product (models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    @property
    def imageURL(self):
        if(self.image==None):
            url='/images/placeholder.png'
        else:
            url = self.image.url
        return url

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    @property
    def finalPrice(self):
        orderitems = self.orderitem_set.all()
        finPrice = sum([item.totPrice for item in orderitems])
        finPrice = round(finPrice,2)
        return finPrice 

    @property
    def finalItemNum(self):
        orderitems = self.orderitem_set.all()
        finNum = sum([item.quantity for item in orderitems])

        return finNum

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def totPrice (self):
        price = round(self.quantity * self.product.price,2)
        
        return price
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=100,null=False)
    state = models.CharField(max_length=100,null=False)
    zipcode = models.CharField(max_length=100,null=False)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.address
    