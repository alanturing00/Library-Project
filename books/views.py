from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import (BooksCatalogsSerializer, BooksSerializer, RentalBookSeriliazer,
                          ReviewSerializer, UserRentalBookSeriliazer, UserProfileUpdateSerializer,RegisterSerializer,
                          UserPasswordChangserializer, ReviewSerializer, UserSerializer,
                           UserProfileserializer, BookSerializer, Bookrentalserializer)
from rest_framework.response import Response
from .models import Book, Review, UserProfile, Rental
from .permissions import IsAdminOrReadOnly, IsMyAcountOrReadOnly, IsAdmin
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

# signup view:
@extend_schema(
    description="sign up view, username and password are requeried, u need to use the api/v1/api/token/ to get the access key after this step, than put it inside the 'berrar' field.",
    summary="signup a new user",
    tags=["user-stuff"])
class RegisterUserAPIView(APIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer
  def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



# change password:
@extend_schema(
    description="change the authenticated user his password",
    summary="update user password",
    tags=["user-stuff"])
class ChangePasswordView(generics.UpdateAPIView):
    model = User
    serializer_class =UserPasswordChangserializer
    permission_classes = [IsAuthenticated,]
    
    def get_object(self,queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if self.object.check_password(serializer.data.get('old_password')):
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response ={
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Your password has been changed succesfully',
                    'data':[]
                }
                return Response(response)
            else:
                Response({'old_password':['wrong password. ']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# view all the catalogs:
@extend_schema(
    description="view all the cataloges list",
    summary="catalogs list",
    tags=["book-stuff"])
class BooksCatalogs(generics.ListAPIView):
    serializer_class= BooksCatalogsSerializer
    permission_classes= [IsAuthenticated,]
    authentication_classes= [JWTAuthentication,]
    
    def get_queryset(self):
        return Book.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        catalogs = queryset.values_list('cataloge', flat=True).distinct()
        data = {'user': user_data, 'books': list(catalogs)}
        return Response(data)
    

# view all books inside the catalog:
@extend_schema(
    description="view all the books inside a custom cataloge",
    summary="view books list inside a cataloge",
    tags=["book-stuff"])
class BooksByCatalogs(generics.ListAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= BooksSerializer 
    
    def get_queryset(self):
        catalogs= self.kwargs['catalogs']
        books= Book.objects.filter(cataloge=catalogs)
        return books
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        data = {'user': user_data, 'books':BooksSerializer(queryset, many= True).data}
        return Response(data)



# view the book details:
@extend_schema(
    description="veiw the book details and allowing user to submet a review",
    summary="book details and allowing the user to submit a review from (0 to 5) and a comment on the book",
    tags=["book-stuff"])
class BookDetails(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= ReviewSerializer

    def get_queryset(self):
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        review= Review.objects.filter(book= book)
        return review
    
    def list(self, request, *args, **kwargs):
        # profile= UserProfile.objects.get(user= self.request.user)
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        reviews= self.get_queryset()
        reviews_serializer= ReviewSerializer(reviews, many=True)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        book_serializer = BooksSerializer(book)
        data = {'user': user_data, 'books': book_serializer.data, 'reviews': reviews_serializer.data}
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        profile= UserProfile.objects.get(user= self.request.user)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        seriliazer= ReviewSerializer(data= request.data)
        if seriliazer.is_valid():
            seriliazer.save( user= profile, book= book)
            return Response(seriliazer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "an error occurred during save the comment!"}, status=status.HTTP_400_BAD_REQUEST)
    


# user profile:
@extend_schema(
    description="view the user profile",
    summary="view the user profile and the books that he rent",
    tags=["user-stuff"])
class UserProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileserializer

    def get_queryset(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        return Rental.objects.filter(user=profile)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        user_books_serializer = UserRentalBookSeriliazer(queryset, many=True)
        profile_serializer = UserProfileserializer(profile)
        user_serializer = UserSerializer(user)

        data = {
            'user': user_serializer.data['username'],
            'profile': profile_serializer.data,
            'rental_book': user_books_serializer.data
        }
        return Response(data)


# update the user profile:
@extend_schema(
    description="update the user information",
    summary="update the user information, the address and the photo, but the photo must be encripted!",
    tags=["user-stuff"])
class UserProfileUpdate(generics.RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= UserProfileUpdateSerializer

    def get_object(self):
        user= self.request.user
        return UserProfile.objects.get(user=user)


# rent a book:
@extend_schema(
    description="rent a book",
    summary="endpoint to rent a book, user how make the request can rent the book if the book count over 0, user will rent the book just for 10 dayes",
    tags=["book-stuff"])
class RentalBook(generics.CreateAPIView):
    permission_classes= (IsAuthenticated,)
    serializer_class= RentalBookSeriliazer

    def create(self, request, *args, **kwargs):
        profile= UserProfile.objects.get(user= self.request.user)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        serializer= RentalBookSeriliazer(data= request.data)
        if serializer.is_valid():
            # user only have one object of the same book:
            try:
                B= Rental.objects.get(user= profile, book=book)
                return Response({"error": "You alredy rent this book!"}, status=status.HTTP_400_BAD_REQUEST)
            
            except Rental.DoesNotExist:
                serializer.save(user= profile, book= book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)