from django.db import models
from django.contrib.auth.models import User
import os
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date, timedelta

def get_upload_path(instance, filename):
    # Get the username of the user
    username = instance.user.username
    # Create a folder with the username if it doesn't exist
    folder_path = os.path.join('media', username)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Return the path where the file will be stored
    return os.path.join(folder_path, filename)


def get_upload_book_path(instance, filename):
    # Get the username of the user
    bookname = instance.title
    # Create a folder with the username if it doesn't exist
    folder_path = os.path.join('book_media', bookname)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Return the path where the file will be stored
    return os.path.join(folder_path, filename)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_photo = models.ImageField(upload_to=get_upload_path, height_field=None, width_field=None, max_length=None, null=True, blank=True)
    address = models.TextField(max_length=35, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    CalalogList=[("Art","art"), ("Music","music"), ("Luctcer","luctcer"), ("Since","since"), ("Technology","technology")]
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    cataloge= models.CharField(choices=CalalogList, max_length=50, null=False, blank=True) 
    isbn = models.CharField(max_length=14)
    copycounts = models.IntegerField(default=0)
    publishe_date= models.DateField(auto_now_add=True, null=True, blank=True)
    cover_photo = models.ImageField(upload_to=get_upload_book_path, height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    
def default_due_date():
    return date.today() + timedelta(days=10)
class Rental(models.Model):
    book = models.ForeignKey(Book ,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_rental = models.DateField(auto_now_add=True)
    date_to = models.DateField(default=default_due_date)
    additional_information= models.TextField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.user.user.username} rented {self.book.title}"

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='r_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user_review_of_five = models.IntegerField(null = True, blank=True)
    user_review_comment = models.TextField(max_length=200, null=True, blank=True)
    review_date= models.DateField( auto_now_add= True)
    def __str__(self):
        return f"{self.user.user.username} has review {self.book.title} book"