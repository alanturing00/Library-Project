from django.urls import path
from .views import (BooksCatalogs, BooksByCatalogs, BookDetails, RentalBook, UserProfileUpdate
                    ,ChangePasswordView, UserProfileView,RegisterUserAPIView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # user stuff:
    # signup:
    path("signup/", RegisterUserAPIView.as_view(), name= "RegisterUserAPIView"),
    # token key:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # refresh the token:
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # update the password:
    path('user/change_password/update/',ChangePasswordView.as_view(),name='changepass'),
    # to veiw the user profile:
    path('user/profile/', UserProfileView.as_view(), name='userprofile'),
    # to edite the user profiel information:
    path("user/profile/update/", UserProfileUpdate.as_view(), name="userprofileupdate"),


    # books stuff:
    # to veiw all the catalogs of the books:
    path("books/catalogs/", BooksCatalogs.as_view(), name="catalogname"),
    # to view the book inside the catalog:
    path("books/catalogs/<str:catalogs>/", BooksByCatalogs.as_view(), name="books"),
    # to view the book details:
    path("books/catalogs/<str:catalogs>/<str:isbn>/", BookDetails.as_view(), name="bookdetails"),
    # to rente books:
    path("books/catalogs/<str:catalogs>/<str:isbn>/rental/", RentalBook.as_view(), name="rentalbook"),
    # add review book:
    # path('books/catalogs/<str:catalogs>/<int:pk>/reviews/', BookReviewList.as_view(), name='book_reviews'),

]
