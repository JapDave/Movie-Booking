from django.db import models
from django.shortcuts import render,redirect
from .models import *
from .views import *


def obj(request, oid):
       data = Movies.objects.get(id=oid)
       data.delete()
       return redirect(Deletemovie)