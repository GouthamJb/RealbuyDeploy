from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class PropertyDetails(models.Model):
    saleORrent = models.CharField(max_length=10, blank=False, default='')
    propertytype = models.CharField(max_length=50, blank=False, default='')
    propertyphoto = models.ImageField(upload_to='images/')
    city = models.CharField(max_length=50, blank=False, default='')
    address = models.CharField(max_length=200, blank=False, default='')
    price = models.CharField(max_length=50, blank=False, default='')
    bedroom = models.IntegerField()
    bathroom = models.IntegerField()
    buildingarea = models.CharField(max_length=50, blank=False, default='')
    carpetarea = models.CharField(max_length=50, blank=False, default='')
    transcationtype = models.CharField(max_length=50, blank=False, default='')
    propertyfloor = models.IntegerField()
    totalfloor = models.IntegerField()
    ownership = models.CharField(max_length=50)
    availability = models.CharField(max_length=50, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    latitude = models.CharField(max_length=50, default='')
    longitude = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=50, default='')
    selleraddress = models.CharField(max_length=100, default='')
    sellername = models.CharField(max_length=100,default='')
    
    
    class Meta:
        ordering =['-id']
    def __str__(self):
        return str(self.id)
class UserProfile(AbstractUser):
    phone = models.CharField(_("phone"),max_length=50)
    address = models.CharField(_("address"),max_length=100,default='')
    favorites = models.ManyToManyField(PropertyDetails,related_name='favorited_by')

class ProfilePicture(models.Model):
    username = models.CharField(max_length=50, blank=False, default='')
    profilephoto = models.ImageField(upload_to='images/')
    

    def __str__(self):
        return self.username


class Recent(models.Model):
    username=models.CharField(max_length=100,default='')
    PropertyDetails=models.ForeignKey(PropertyDetails,on_delete=models.CASCADE)
    datetime = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.username