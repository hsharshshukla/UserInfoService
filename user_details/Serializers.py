from  django.http import JsonResponse
from rest_framework import serializers
from .models import UserDetail,Email,Phone


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email']

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['phone']

class UserSerializer(serializers.ModelSerializer):
    email = EmailSerializer(many=True,read_only=True,source='emails')
    phone = PhoneSerializer(many=True,read_only=True,source='phones')
    class Meta:
        model = UserDetail
        fields = ('user_id','first_name','last_name','full_name','email','phone')
        
   
class UserCreateSerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True)
    phones = PhoneSerializer(many=True)
    class Meta:
        model = UserDetail
        fields = ['first_name','last_name','full_name','phones','emails']
    
    def create(self, validated_data):
        email_data = validated_data.pop('emails')
        phone_data = validated_data.pop('phones')
        
        userdetail = UserDetail.objects.create(**validated_data)
        
        for e  in email_data:
            Email.objects.create(**e,user_id = userdetail)
        for p in phone_data:
            Phone.objects.create(**p,user_id=userdetail)
        return userdetail
