# Generated by Django 3.2.3 on 2021-06-10 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_book', '0003_movies_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail id')),
                ('password', models.CharField(max_length=50, verbose_name='password')),
            ],
        ),
    ]
