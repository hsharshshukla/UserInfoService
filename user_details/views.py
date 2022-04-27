from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
from functools import reduce
import operator
from django.db.models import Q
from .Serializers import UserSerializer,EmailSerializer,PhoneSerializer,UserCreateSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UserDetail,Email,Phone
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
def user_create(request,*args,**kwargs):
    """Converting email & phones list to dict"""
    i=0
    for d in request.data:
        d = d['phones']
        p=[]
        for a in d :
            ae={}
            ae['phone']=a
            p.append(ae)
        request.data[i]['phones']=p
        i =i+1
        
    j=0
    for xp in request.data:
        xp = xp['emails']
        p=[]
        for a in xp :
            pe={}
            pe['email']=a
            p.append(pe)
        request.data[j]['emails']=p
           
        j =j+1

    serializer = UserCreateSerializer(data=request.data,many=True)
    serializer.is_valid()
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({'Success':f'Users Created in System'},status=200)
    else :
        return JsonResponse(serializer.errors, status=400,safe=False)
    
@api_view(['GET'])
def get_user_by_id(request,*args,**kwargs):
    try:
        print(request.data)
        id_list = request.data['ids']
        print(id_list)
        print(request.data)
        u = UserDetail.objects.filter(user_id__in=id_list)
        return get_paginated_queryset_response(u,request)
            
    except:
        return JsonResponse({"message":"User Not Found"},status=404,safe=False)


@api_view(['GET'])
def get_user_by_name(request,*args,**kwargs):
    try:
        print(request.data)
        name_list = request.data['names']
        print(name_list)
        
        clauses = (Q(full_name__icontains=n) for n in name_list)
        query = reduce(operator.or_,clauses)
        print(query)
        u = UserDetail.objects.filter(query)
        print(u)
        return get_paginated_queryset_response(u,request)
        
    except:
        return JsonResponse({'message':'Please check names List'},status=400)

@api_view(['PUT'])
def delete_user_by_id(request,*args,**kwargs):
    try:
        print(request.data)
        user_list = request.data['ids']
        print(user_list)
        if UserDetail.objects.filter(user_id__in=user_list).exists():      
            obj = UserDetail.objects.filter(user_id__in=user_list).delete()
            deleted_count = len(obj)-1
            return JsonResponse({'message':f'User Deleted! Deleted User Count = {deleted_count}'},status=200)   
        else:
            return JsonResponse({"message":"Users in List Not Found in System"},status=404)
    except:
        return JsonResponse({'Error':'Invalid Json Data'},status=400)

@api_view(['PUT'])
def update_contact(request,*args,**kwargs):
    
    """Fetch Paramters from Request query_params"""
    # print(request.data)
    for d in request.data:
        contact_type = d['contact_type']
        flag = d['flag']
        user_id = d['user_id']
        old_contact = d['old_contact']
        new_contact = d['new_contact']
       
        # check for required attributes to modify Email info of user
        if contact_type not in['Email','Phone'] or flag ==None or user_id ==None:
            return JsonResponse({"message":f'Please input Update/Add flag, Contact, and User_id Details'},status=400)
        
        try:
            if contact_type == 'Email' :        
                return update_email(flag,user_id,new_contact,old_contact)    
            elif contact_type == 'Phone':
                return update_phone(flag,user_id,new_contact,old_contact)  
            
        except:
            return JsonResponse({'message':'Invalid Inputs'},status=400)

    return JsonResponse({'Info':'No data passed'},status=200)


"""Supporting Funn"""
#Update Email    
def update_email(flag,user_id,new_email,old_email):
    try:

        if flag=='0': #update existing
            Email.objects.filter(email=old_email).update(email=new_email)
            return JsonResponse({'Success':f'Email {new_email} updated for user id {user_id}'},status=200)
        elif flag=='1':   # Add new 
            print('flag 1',new_email)
            # print(Email.objects.filter(email=new_email).exists())
            if Email.objects.filter(email=new_email).exists():
                return JsonResponse({'Warning':f'Email {new_email} Already Exists'},status=200)
            else:
                u = UserDetail.objects.get(user_id=user_id)
                Email.objects.create(email=new_email,user_id=u)
                return JsonResponse({'Success':f'Email {new_email} Added for user {user_id}'},status=200)
        else:
            return JsonResponse({'Error':'wrong Flag'},status=400)
    except:
        return JsonResponse({'Error':'Email Update Failed'},status=400)

#Update Phone
def update_phone(flag,user_id,new_phone,old_phone):
    try:
        if flag=='0': #update existing
            Phone.objects.filter(phone=old_phone).update(phone=new_phone)
            return JsonResponse({'message':'phone updated'},status=200)
        else:   # Add new 
            if Phone.objects.filter(phone=new_phone).exists():
                return JsonResponse({'message':'phone {new_phone} Already Exists {user_id}'},status=200)
            else:
                u = UserDetail.objects.get(user_id=user_id)
                Phone.objects.create(phone=new_phone,user_id=u)
                return JsonResponse({'message':'phone {new_phone} Added for user {user_id}'},status=200)
    except:
        return JsonResponse({'Error':'Phone Update Failed'},status=400)

def get_paginated_queryset_response(qs,request):
    paginator = PageNumberPagination()
    paginator.page_size=20
    paginated_qs = paginator.paginate_queryset(qs,request)
    print(paginated_qs)
    serializer = UserSerializer(paginated_qs,many=True)
    return paginator.get_paginated_response(serializer.data)