# Generated by Django 4.2.1 on 2023-05-22 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_rename_book_id_rental_book_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rental',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='user_id',
            new_name='user',
        ),
    ]