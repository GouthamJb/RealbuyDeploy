from rest_framework import serializers
from .models import PropertyDetails,ProfilePicture

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyDetails
        fields = ('id','saleORrent','propertytype','propertyphoto','city','address','price','bedroom','bathroom','buildingarea','carpetarea','transcationtype','propertyfloor','totalfloor','ownership','availability','description','latitude','longitude','phone','email')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePicture
        fields =('profilephoto',)