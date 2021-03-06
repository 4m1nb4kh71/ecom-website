from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer (models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    

class Store(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=False,blank=False)
    storename = models.CharField(max_length=20)
    def __str__(self):
        return str(self.storename)

class Product (models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE,null=False,blank=False)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    
    description = models.CharField(default=None,blank=True,max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    @property
    def imageURL(self):
        if(self.image):
            url = self.image.url
        else:
            url='/images/placeholder.png'
        return url

    def __str__(self):
        return str(self.name)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    @property
    def finalPrice(self):
        orderitems = self.orderitem_set.all()
        finPrice = 0
        for item in orderitems :
            if item.product !=None:
                finPrice +=item.totPrice
        
        finPrice = round(finPrice,2)
        return finPrice 

    @property
    def finalItemNum(self):
        orderitems = self.orderitem_set.all()
        finNum = 0 
        for item in orderitems:
            if item.product !=None:
                finNum += item.quantity
        

        return finNum

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems :
            if i.product !=None: 
                if i.product.digital == False:
                    shipping = True
        return shipping

    def __str__(self):
        return str(self.id)

    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def totPrice (self):
        if self.product != None:
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
    