from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Menu(models.Model):
      user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
      dish_name=models.CharField(max_length=100,null=True,blank=True)
      category=models.CharField(max_length=100,null=True,blank=True)
      image=models.ImageField(null=True,blank=True)
      description=models.TextField(max_length=200,null=True,blank=True)
      rating=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
      numReviews=models.IntegerField(null=True,blank=True,default=0)
      price=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
      counterInStock=models.IntegerField(null=True,blank=True,default=0)
      createdAt=models.DateTimeField(auto_now_add=True)
      _id=models.AutoField(primary_key=True,editable=False)
      def __str__(self):
          return str(self.dish_name)

class OrderStatus(models.Model):
    
    isReady= models.BooleanField(default=False,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)
    paidAt = models.DateTimeField(auto_now_add=False,null=True)
    def __str__(self):
        return str(self._id)


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    dish = models.ForeignKey(Menu,on_delete=models.SET_NULL,null=True)
    orderStatus = models.ForeignKey(OrderStatus,on_delete=models.SET_NULL,null=True)
    #qty = models.IntegerField(null=True,blank=True,default=0)
    paymentMethod = models.CharField(max_length=100,null=True,blank=True)
    isPaid= models.BooleanField(default=False)
    taxPrice = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    totalPrice = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    paidAt = models.DateTimeField(auto_now_add=False,null=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)
    def __str__(self):
        return str(self._id)

class OrderItem(models.Model):
    menu = models.ForeignKey(Menu,on_delete=models.SET_NULL,null=True)
    order =  models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    qty = models.IntegerField(null=True,blank=True,default=0)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    image = models.CharField(max_length=100,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)
    def __str__(self):
        return str(self.name)







    

