from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review,UserProfile, Rental
import base64
from django.contrib.auth.hashers import make_password

# user stuff:

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['username','email','password','first_name','last_name']
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(RegisterSerializer, self).create(validated_data)

# used!
class UserPasswordChangserializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required =True)
    new_password = serializers.CharField(required =True) 

# used!
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= UserProfile
        fields= ["user_photo",'user']


class UserProfileForReview(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_photo','id']


# Book Stuff


# used!
class BooksCatalogsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= ['cataloge']


# used!
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= ['title', 'author', 'cover_photo', 'cataloge', 'copycounts', 'isbn']

class ReviewSerializer(serializers.ModelSerializer):
    user_review_of_five= serializers.CharField()
    user_review_comment= serializers.CharField()
    class Meta:
        model= Review
        fields= ["user_review_of_five", "user_review_comment", "review_date"]


# used!
class UserProfileserializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['address', 'user_photo']
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields= ['address','user_photo']

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        if validated_data.get('user_photo'):
            instance.user_photo.delete()
            instance.user_photo = validated_data.get('user_photo')
        instance.save()
        return instance

# used!
class RentalBookSeriliazer(serializers.ModelSerializer):
    
    class Meta:
        model= Rental
        fields= ['date_to', 'additional_information']
    
class UserRentalBookSeriliazer(serializers.ModelSerializer):
    
    class Meta:
        model= Rental
        fields= "__all__"




class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= '__all__'


class Bookrentalserializer(serializers.ModelSerializer):
    date_to= serializers.DateField(required= True)
    additional_information= serializers.CharField(required=True)
    user= UserProfileForReview(read_only= True)
    book= BookSerializer(read_only= True)
    class Meta:
        model =Rental
        fields =['id', 'date_rental', 'date_to', 'additional_information', 'book', 'user']

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required= True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user










