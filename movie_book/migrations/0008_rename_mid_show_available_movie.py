# Generated by Django 3.2.3 on 2021-06-13 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_book', '0007_auto_20210613_2011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show_available',
            old_name='mid',
            new_name='movie',
        ),
    ]
