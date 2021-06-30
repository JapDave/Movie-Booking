from os import name
from django.conf.urls import url
from django.urls import path
from .views import *
#from .obj_views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('Forgetpassword',Forget_password,name='Forgot_Password'),
   path('otp_verify',otp_verify,name='otp_verify'),
   path('Newpassword',New_password,name='New_Password'),
   # USER SECTION 

   path('',index,name='index'),
   path('Movies/',movies,name='Movies'),
   path('/User_Login',User_Login,name='User_Login'),
   path('/User_Registration',User_Registration,name='User_Registration'),
   path('/User_Logout',User_Logout,name='User_Logout'),
   path('BookShow/<int:id>',Book_show,name='Book_show'),
   path('BookShow_tom/<int:id>',Book_show_tom,name='Book_show_tommorrow'),
   path('Ticketsection/<int:id>',Ticket_No,name='No_ticket'),
   path('seat_selection',seat_selection,name='Seat_selection'),
   path('payment',payment,name='payment'),

   # ADMIN SECTION

   path('Login',login,name='login'),
   path('Logout',Logout,name='Logout'),
   path('Dashboard',Dashboard,name='Dashboard'),
   path('AddMovie',Addmovie,name='Addmovie'),
   path('DeleteMovie',Deletemovie,name='Deletemovie'),
   path('objD/<did>',objD,name='objD'),
   path('objU/(?P<mid>[0-9]+)/$',objU,name='objU'),
   path('UpdateMovie',Updatemovie,name='Updatemovie'), 
   path('AddTheatre',Add_Theatre,name='AddTheatre'),

   # THEATRE SECTION

   path('Theatre/Theatre_Login',Theatre_Login,name='Theatre_Login'),
   path('Theatre/Theatre_Logout',Theatre_Logout,name='Theatre_Logout'),
   path('Theatre/Dashboard',Theatre_index,name='Theatre_Dashboard'),
   path('Theatre/Add_show/<int:id>',Add_show,name='Add_show'),
 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)