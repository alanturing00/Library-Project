from django.contrib import admin

from .models import Book, UserProfile, Review, Rental

admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rental)