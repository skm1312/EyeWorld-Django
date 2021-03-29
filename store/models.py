from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import validate_email
# Create your models here.


class ProductCategories(models.Model):

    name = models.CharField(max_length=100,blank=False,null=True)
    image = models.ImageField(null=True,blank=False)

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

class FaceShape(models.Model):

    name = models.CharField(max_length=100,blank=False,name=False)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Prescription(models.Model):
    
    name = models.CharField(max_length=50, null= False, default = "")
    prescription = models.CharField(max_length=255, null= False, default = "")
    prescriptionImage = models.ImageField(upload_to='images/pres/')
    
    def __str__(self):
        return self.name

class Product(models.Model):

    category = models.ManyToManyField(ProductCategories)
    name = models.CharField(max_length=100,blank=False,name=False)
    price = models.FloatField(blank=False,null=False)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    shape = models.CharField(max_length=100,null=True,blank=False)

    def __str__(self):
        return self.name

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class OrderItem(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return '{}-{}'.format(self.user.username,self.product.name)



class ShippingAddress(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)
    recepient_fullname = models.CharField(max_length=100,null=True,blank=False)
    phone_no = models.IntegerField(null=False,blank=False)
    address_line1 = models.CharField(max_length=200, null=True,blank=False)
    address_line2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=100,null=True,blank=False)
    zipcode = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=100, null=False, default="") 
    date_added = models.DateTimeField(auto_now_add=True,null=False)
    
    def __str__(self):
        return '{}-{}'.format(self.address_line1, self.address_line2)



class FullOrder(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    recepient_fullname = models.CharField(max_length=100, null=True, blank=False)
    phone_no = models.IntegerField(null=True, blank=False)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=200, null=True,blank=False)
    state = models.CharField(max_length=200, null=True,blank=False)
    country = models.CharField(max_length=100, null=True, blank=False)
    zipcode = models.CharField(max_length=200, null=True,blank=False)
    amount = models.FloatField(null=True,blank=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    success = models.BooleanField(null=False,default=True)

    def successOrder(self,user_id):
        #user_id = self.user
        print("Mail control for successorder")
        print(user_id)
        adr = ShippingAddress.objects.get(id=user_id)
        #obj = FullOrder.objects.create(user = request.user)


        template = render_to_string('store/email_template.html', {'name':adr.recepient_fullname})


        email = EmailMessage(
            'Thank you for your order2',
            template,
            settings.EMAIL_HOST_USER,
            [adr.email],
            )
        email.fail_silently=False
        email.send()

    def __str__(self):
        return '{}-{}'.format(self.recepient_fullname,self.id)



class Purchased_item(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(FullOrder,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, name=False)
    price = models.FloatField(blank=False, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

    def __str_ (self):
        return self.name

class sendEmail:

    def __init__(self, user_id=[]):
        print("Initialized")
        self.user_id = user_id
        self.Model = FullOrder()

    def sendmail(self, user_id):
        print("sendmail in sendEmail class")
        return self.Model.successOrder(user_id)