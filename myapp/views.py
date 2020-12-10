from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import UserProfile
from .models import PropertyDetails,ProfilePicture,Recent
from .serializers import PropertySerializer,ProfileSerializer
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.



@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")
    address = request.data.get("address")
    print(username,email,)

    if username is None or password is None or email is None or phone is None or address is None:
        return JsonResponse({'error': 'Please provide  username , password, phone,adress and email'})
    try:
        UserProfile.objects.create_user(username=username,password=password,email=email,phone=phone,address=address)
        return JsonResponse({'status': 'success','message':'signup successful'})
    except:
        return JsonResponse({'error': 'User already exists'},status=400)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'},status=400)
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Invalid Credentials'},status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({"status":"success","message":"login successful","data":{"token":token.key}})



@permission_classes((IsAuthenticated,))
@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    return JsonResponse({"status":"success","message":"logout successful"})


@permission_classes((IsAuthenticated,))
@api_view(["POST"])
def changePassword(request):
    oldpassword= request.data.get('oldpassword')
    newpassword= request.data.get('newpassword')

    user=Token.objects.get(key=request.auth.key).user
    if(user.check_password(oldpassword)):
        user.set_password(newpassword)
        user.save()
        return JsonResponse({"status":"success","message":"Change password successful"})
    else:
        return JsonResponse({"error":"invalid credentials"},status=400)

@permission_classes((IsAuthenticated,))
@api_view(["POST","GET"])
def propertydetails(request):
    if request.method == 'GET':
        user=Token.objects.get(key=request.auth.key).user
        propertydetails=PropertyDetails.objects.filter(saleORrent="sale")
        paginator = Paginator(propertydetails,3)
        page_no = request.GET.get('page')
        page_details = paginator.get_page(page_no).object_list
        
        property_serializer = PropertySerializer(page_details,many=True)
        
        new_serializer_data = list(property_serializer.data)
        for i in range(0,len(new_serializer_data)):
            if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id'],username=user).exists()):
                 new_serializer_data[i].update({'favorites':True})
            else:
                new_serializer_data[i].update({'favorites':False})
            

        pagecount = int(paginator.num_pages)
        new_serializer_data.append({'pagecount':pagecount})
    
        return JsonResponse(new_serializer_data ,safe=False)
    elif request.method == 'POST':
        user=Token.objects.get(key=request.auth.key).user
        
        
        
        saleORrent = request.data.get('saleORrent')
        propertytype= request.data.get('propertytype')
        propertyphoto= request.data.get('propertyphoto')
        city = request.data.get('city')
        address= request.data.get('address')
        price = request.data.get('price')
        bedroom= request.data.get('bedroom')
        bathroom= request.data.get('bathroom')
        buildingarea = request.data.get('buildingarea')
        carpetarea = request.data.get('carpetarea')
        transactiontype = request.data.get('transactiontype')
        propertyfloor = request.data.get('propertyfloor')
        totalfloor = request.data.get('totalfloor')
        ownership = request.data.get('ownership')
        availability = request.data.get('availability')
        description = request.data.get('description')
        latitude= request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        phone=user.phone
        email=user.email
        selleraddress = user.address
        sellername = user.username
        PropertyDetails.objects.create(
            saleORrent=saleORrent,
            propertytype=propertytype,
            propertyphoto=propertyphoto,
            city=city,
            address=address,
            price=price,
            bedroom=bedroom,
            bathroom=bathroom,
            buildingarea=buildingarea,
            carpetarea=carpetarea,
            transcationtype=transactiontype,
            propertyfloor=propertyfloor,
            totalfloor=totalfloor,ownership=ownership,
            availability=availability,
            description=description,
            latitude=latitude,longitude=longitude,
            phone=phone,
            email=email,selleraddress=selleraddress,
            sellername=sellername
        )
        return JsonResponse({"status":"success"})





@permission_classes((IsAuthenticated,))
@api_view(["POST"])
def searchdetails(request):
    searchcity = request.data.get('searchcity')
    
    searchresult = PropertyDetails.objects.filter(city__icontains=searchcity)
    
    search_serializer = PropertySerializer(searchresult,many=True)
    return JsonResponse(search_serializer.data,safe=False)


@permission_classes((IsAuthenticated,))
@api_view(["POST","GET"])
def profilepicture(request):
    if(request.method == "POST"):
        profilepicture = request.data.get('profilepicture')
        
        
        user=Token.objects.get(key=request.auth.key).user
        
        if(ProfilePicture.objects.filter(username=user).exists()):
            oldpicture=ProfilePicture.objects.filter(username=user)
            oldpicture.delete()
            ProfilePicture.objects.create(username= user,profilephoto =  profilepicture)
            return JsonResponse({"status":"succesfully addded new image"})
        else:
            ProfilePicture.objects.create(username= user,profilephoto =  profilepicture)
            return JsonResponse({"status":"success"})


    elif(request.method == "GET"):
        user=Token.objects.get(key=request.auth.key).user
        
        pictureresult = ProfilePicture.objects.filter(username=user)
        
        picture_serializer = ProfileSerializer(pictureresult,many=True)
        new_picture_serializer = list(picture_serializer.data)
        new_picture_serializer.append({'username':user.username,'address':user.address})
        return JsonResponse(new_picture_serializer,safe=False)
        
@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def rent(request):
    
    propertydetails=PropertyDetails.objects.filter(saleORrent="rent")
    user=Token.objects.get(key=request.auth.key).user
    paginator = Paginator(propertydetails,3)
    page_no = request.GET.get('page')
    page_details = paginator.get_page(page_no).object_list
    
    property_serializer = PropertySerializer(page_details,many=True)
    new_serializer_data = list(property_serializer.data)
    for i in range(0,len(new_serializer_data)):
        if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id'],username=user.username).exists()):
            new_serializer_data[i].update({'favorites':True})
        else:
            new_serializer_data[i].update({'favorites':False})
    pagecount = int(paginator.num_pages)
    new_serializer_data.append({'pagecount':pagecount})
    
    return JsonResponse(new_serializer_data ,safe=False)

@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def readytomove(request):
    propertydetails=PropertyDetails.objects.filter(availability="ready to move")
    user=Token.objects.get(key=request.auth.key).user
    paginator = Paginator(propertydetails,3)
    page_no = request.GET.get('page')
    page_details = paginator.get_page(page_no).object_list
    
    property_serializer = PropertySerializer(page_details,many=True)
    new_serializer_data = list(property_serializer.data)
    for i in range(0,len(new_serializer_data)):
        if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id'],username=user).exists()):
            new_serializer_data[i].update({'favorites':True})
        else:
            new_serializer_data[i].update({'favorites':False})
    pagecount = int(paginator.num_pages)
    new_serializer_data.append({'pagecount':pagecount})
    
    return JsonResponse(new_serializer_data ,safe=False)
@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def underconstruction(request):
    propertydetails=PropertyDetails.objects.filter(availability="underconstruction")
    user=Token.objects.get(key=request.auth.key).user
    paginator = Paginator(propertydetails,3)
    page_no = request.GET.get('page')
    page_details = paginator.get_page(page_no).object_list
    
    property_serializer = PropertySerializer(page_details,many=True)
    new_serializer_data = list(property_serializer.data)
    for i in range(0,len(new_serializer_data)):
        if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id'],username=user).exists()):
            new_serializer_data[i].update({'favorites':True})
        else:
            new_serializer_data[i].update({'favorites':False})
    pagecount = int(paginator.num_pages)
    new_serializer_data.append({'pagecount':pagecount})
    
    return JsonResponse(new_serializer_data ,safe=False)

@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def accountdetails(request):
    user=Token.objects.get(key=request.auth.key).user
    data={
        "username" : user.username,
        "email" : user.email,
        "phone" : user.phone,
        "address" : user.address
    }
    return JsonResponse(data)


@permission_classes((IsAuthenticated,))
@api_view(["GET","POST"])
def favorite(request):
    if(request.method=="GET"):
        user=Token.objects.get(key=request.auth.key).user
        propertydetails=user.favorites.all()
        paginator = Paginator(propertydetails,3)
        page_no = request.GET.get('page')
        page_details = paginator.get_page(page_no).object_list
    
        property_serializer = PropertySerializer(page_details,many=True)
        new_serializer_data = list(property_serializer.data)
        
        for i in range(0,len(new_serializer_data)):
            if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id']).exists()):
                new_serializer_data[i].update({'favorites':True})
            else:
                new_serializer_data[i].update({'favorites':False})
        pagecount = int(paginator.num_pages)
        new_serializer_data.append({'pagecount':pagecount})
    
        return JsonResponse(new_serializer_data ,safe=False)
    
    elif(request.method=="POST"):
        propertyId = request.data.get('propertyId')
        user=Token.objects.get(key=request.auth.key).user
        print(user)
        propertydetails = PropertyDetails.objects.get(id=propertyId)
        if(UserProfile.objects.filter(favorites=propertyId,username=user.username).exists()):
            user.favorites.remove(propertydetails)
            return JsonResponse({'status':"deleted"})
        else:
            user.favorites.add(propertydetails)
            return JsonResponse({'status':"added"})

@permission_classes((IsAuthenticated,))
@api_view(["GET","POST"])
def recent(request):
    if(request.method=="POST"):
        propertyId = request.data.get('propertyId')
        user = Token.objects.get(key=request.auth.key).user
        date_time = datetime.now()
        print(date_time)
        propertydetails = PropertyDetails.objects.get(id=propertyId)
        if(Recent.objects.filter(username=user.username,PropertyDetails=propertydetails).exists()):
            recent_data = Recent.objects.get(username=user.username,PropertyDetails=propertydetails)
            recent_data.datetime=date_time
            recent_data.save()
            return JsonResponse({'status':'modified'})
        else:
            if(Recent.objects.filter(username=user.username).count()>=9):
                Recent.objects.filter(username=user.username)[0].delete()
            
            Recent.objects.create(username=user.username,PropertyDetails=propertydetails,datetime=date_time)
            return JsonResponse({'status':'added'})
    elif(request.method=="GET"):
        user = Token.objects.get(key=request.auth.key).user
        propertydetail=PropertyDetails.objects.all().filter(recent__username=user.username).order_by('-recent__datetime')
        print(propertydetail)
        paginator = Paginator(propertydetail,3)
        page_no = request.GET.get('page')
        page_details = paginator.get_page(page_no).object_list
    
        property_serializer = PropertySerializer(page_details,many=True)
        new_serializer_data = list(property_serializer.data)
        for i in range(0,len(new_serializer_data)):
            if(UserProfile.objects.filter(favorites=new_serializer_data[i]['id'],username=user.username).exists()):
                new_serializer_data[i].update({'favorites':True})
            else:
                new_serializer_data[i].update({'favorites':False})
        pagecount = int(paginator.num_pages)
        new_serializer_data.append({'pagecount':pagecount})
    
        return JsonResponse(new_serializer_data ,safe=False)