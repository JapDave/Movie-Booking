#from movie_magic.movie_book.models import movies
#from movie_magic.movie_book.models import Admin, Movies
from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Movies)
admin.site.register(Admin)
admin.site.register(Users)
admin.site.register(Theatre)
admin.site.register(Show_available)
admin.site.register(Payment)