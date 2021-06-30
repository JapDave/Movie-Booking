from django.db import reset_queries
from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
import random,smtplib
from email.message import EmailMessage
from datetime import date, timedelta
import os

# Create your views here.

#---------  FORGET PASSWORD START ------------------------------------------
def Forget_password(request):
        if request.POST:
                email = request.POST['uemail']
                user_data = Users.objects.get(Email=email)
                theatre_data = Theatre.objects.get(Email=email)
                admin_data = Admin.objects.get(email=email)

                no = "1234567890"
                otp = ""
                for x in range(4):
                         otp += random.choice(no)
                
                request.session['otp'] = otp 
                if user_data:
                        email = user_data.Email
                        request.session['otp_user'] = email
                elif theatre_data:
                        email = theatre_data.Email
                        request.session['otp_user'] = email
                elif admin_data: 
                        email = admin_data.email
                        request.session['otp_user'] = email
                        
                sender_email="moviemagic616@gmail.com"
                sender_pass="tarak1234"
                recv_email=email
                
                server = smtplib.SMTP('smtp.gmail.com',587)

                msg1 = f''' 
                       The OTP for your account access is {otp}
                
                '''

                msg = EmailMessage()
                msg['subject'] = "otp for an account verification"
                msg['From']=sender_email
                msg['To']=recv_email
                password_S = sender_pass
                msg.add_header('content-Type','text/html')
                msg.set_payload(msg1)     
                
                server.starttls()
                server.login(msg['From'],password_S)
                server.sendmail(msg['From'],msg['To'],msg.as_string())

                return redirect(otp_verify)

        return render(request,'Forget_password.html')

def otp_verify(request):
        if request.POST:
                user_otp = request.POST['otp']
                gen_otp = request.session['otp']

                if user_otp == gen_otp:
                        
                    return redirect(New_password)

        return render(request,'otp.html')

def New_password(request):
        otp_user = request.session['otp_user']
        user_data = Users.objects.get(Email=otp_user)
        theatre_data = Theatre.objects.get(Email=otp_user)
        admin_data = Admin.objects.get(email=otp_user)
        if request.POST:
               pass1 = request.POST['pass1']
               pass2 = request.POST['pass2']

               if pass1 == pass2:
                      if user_data:
                              user_data.password = pass1
                              user_data.save()
                              return redirect(User_Login)
                      
                      elif theatre_data:      
                             theatre_data.password = pass1
                             theatre_data.save()
                             return redirect(Theatre_Login)

                      elif admin_data:
                              admin_data.password = pass1
                              admin_data.save()    
                              return redirect(login)  
               else:
                       return redirect(New_password)

        return render(request,'New_password.html')

#-------------- FORGET PASSWORD STOP ------------------------------

# --------------  ADMIN SECTION START -----------------------------
def login(request):
        if request.method == "POST":
                data = Admin.objects.all()

                email = request.POST['uid']
                password = request.POST['pass'] 

                for em in data:
                       
                        if email==em.email and password==em.password:
                                request.session['uid']=em.name
                                return redirect(Dashboard)
                                

        
        
        
        return render(request,'admin_side/Admin_Login.html')

def Logout(request):
       if 'uid' in request.session.keys(): 
         del request.session['uid']
         return redirect(login)
       else:
               return redirect(login)

def Dashboard(request):
       
        if 'uid' in request.session.keys():
                return render(request,'admin_side/index.html')

        return redirect(login)

#-------  MOVIES SECTION --------------


def Addmovie(request):
         
         if 'uid' in request.session.keys():  
                if request.method == "POST":
               
                   name = request.POST['mname']
                   cat1=request.POST['mcategory1']
                   cat2=request.POST['mcategory2']
                   rate=request.POST['rate']
                   rdate=request.POST['rdate'] 
                   dur=request.POST['dh']+":"+request.POST['dm']
                   poster=request.FILES['fn']
                   lang=request.POST['lan']
                   city=request.POST.getlist('mcity')
              
            
        
                   res = Movies(mname=name, category=cat1, category2=cat2, rate=rate, rdate=rdate, dur=dur, poster=poster, language=lang, city=city)
                   res.save()
                

                   return render(request,'admin_side/Admin_Add_Movie_Menu.html') 
        
                return render(request,'admin_side/Admin_Add_Movie_Menu.html') 
        
         return redirect(login) 

def Deletemovie(request):
                
                
                if 'uid' in request.session.keys():
                        data = Movies.objects.all()
                        result = {
                                        
                                    'movies' : data

                                }

        
                        return render(request,'admin_side/Admin_Delete_Movie_Menu.html', result)
                return redirect(login) 

def objD(request,did):
    
       if 'uid' in request.session.keys():     
                data = Movies.objects.get(id=did)
                data.delete()
                return redirect(Deletemovie)
       return redirect(login)

def Updatemovie(request):
        
        if 'uid' in request.session.keys():
                 data = Movies.objects.all()
                 result = {
                
                         'movies' : data

                         }

        
                 return render(request,'admin_side/Admin_Update_Movie_Menu.html', result)
        return redirect(login)

def objU(request,mid):
    
        if 'uid' in request.session.keys():
                if request.method == "POST":
                  mid = int(mid)   
                  #data = Movies.objects.get(id=uid)
                  name = request.POST['mname']
                  cat1=request.POST['mcategory1']
                  cat2=request.POST['mcategory2']
                  rate=request.POST['rate']
                  rdate=request.POST['rdate'] 
                  dur=request.POST['dh']+":"+request.POST['dm']
                  poster=request.FILES['fn']
                  lang=request.POST['lan']
                  city=request.POST.getlist('mcity')
              

                  res = Movies(id=mid,mname=name, category=cat1, category2=cat2, rate=rate, rdate=rdate, dur=dur, poster=poster, language=lang, city=city)  
                  res.save() 
                  return redirect(Updatemovie)



                data = Movies.objects.get(id=mid)
                print(data)
                result = {
                        
                        'movies':(data)
                        }
      
                return render(request,'admin_side/update_Movie.html',result)
        return redirect(login)

#------------ Movie SECTION OVER--------------------

def Add_Theatre(request):
       if 'uid' in request.session.keys():
              
                parent_dict = os.path.dirname(os.path.dirname(__file__))+'\\movie_book\\templates\\user_side\\theatre\\'
                print(parent_dict)
                if request.POST:
                       name=request.POST['tname']
                       email=request.POST['email']
                       contact=request.POST['contact']
                       city=request.POST['city']
                       total_screen=request.POST['screen']
                       lstr = "qwertyuioplkjhgfdsazxcvbnm"
                       ustr = lstr.upper()
                       no = "1234567890"
                       spec = "@#$%^&"

                       temp = lstr+ustr+no+spec
                       password=""
                       for x in range(8):
                         password += random.choice(temp)
                         print(password)


                       data = Theatre(Name=name,Email=email,contact=contact,city=city,total_screen=total_screen,password=password)
                       data.save()

                       path = os.path.join(parent_dict,name)
                       os.mkdir(path)
                       
                       sender_email="moviemagic616@gmail.com"
                       sender_pass="tarak1234"
                       recv_email=email
                       
                       server = smtplib.SMTP('smtp.gmail.com',587)

                       msg1 = f''' 
                                Congratulatiions your account is been activated successfully!!
                                your password is {password} and link for futher service is http://127.0.0.1:8000/Theatre/Theatre_Login
                        
                        '''

                       msg = EmailMessage()
                       msg['subject'] = "your theatre acccount is been successfully activated"
                       msg['From']=sender_email
                       msg['To']=recv_email
                       password_S = sender_pass
                       msg.add_header('content-Type','text/html')
                       msg.set_payload(msg1)     
                       
                       server.starttls()
                       server.login(msg['From'],password_S)
                       server.sendmail(msg['From'],msg['To'],msg.as_string())



                       return render(request,'admin_side/Admin_Add_Theatre.html')
                return render(request,'admin_side/Admin_Add_Theatre.html')       
        
       return redirect(login)

# --------------   ADMIN SECTION  OVER ----------------------------- 


#------------ THEATRE_USER SECTION START------------------

def Theatre_Login(request):
        if request.POST:
                email=request.POST['email']
                password=request.POST['password']
                print(email,password)

                data = Theatre.objects.all()
                for i in data:
                        print(i.Email,i.password)
                        
                        if email == i.Email and password == i.password:
                                
                               request.session['tid']=i.id
                               return redirect(Theatre_index)
                               
                return render(request,'theatre_side/Theatre_Login.html')
                     
        return render(request,'theatre_side/Theatre_Login.html')

def Theatre_Logout(request):
         if 'tid' in request.session.keys():
                 del request.session['tid']
                 return redirect(Theatre_Login)
         else:
                 return redirect(Theatre_Login)        

def Theatre_index(request):
        if 'tid' in request.session.keys():
               theatre_data = Theatre.objects.get(id=request.session['tid'])
               movie_data = Movies.objects.all()
               mov = []
               for i in movie_data:
                    
                        if theatre_data.city in i.city:
                                mov.append(i)
                        
               return render(request,'theatre_side/Home.html',{'theatre':theatre_data,'movies':mov})

        return redirect(Theatre_Login)

def Add_show(request,id):
         if 'tid' in request.session.keys():
              data = Theatre.objects.get(id=request.session['tid'])
              data1 = Movies.objects.get(id=id)
              if request.POST:
                       date = request.POST['date']
                       time = request.POST['time']
                       screen = request.POST['screen']
                       price  = request.POST['price']
                       
                       data = Show_available(movie=data1,Name=data,date=date,time=time,screen=screen,price=price)
                       data.save()
                       return redirect(Theatre_index)
              
              else:  
                return render(request,'theatre_side/Select_show.html')

         else:
        
                return redirect(Theatre_Login)
        





#------------ THEATRE_USER SECTION OVER------------------


     

# -------------- USER SECTION START -----------------------------



def index(request):
        userlist=[]
         
        selected_city=""
        mov=[]
        data = Movies.objects.all()  
       
        if request.method == "POST":   
                selected_city=request.POST['city'] 
                for i in data:
                        if selected_city in i.city :   
                                mov.append(i)
                                request.session['city']=selected_city
                              
        rate_list = []
        top_movies = [] 
        top_city =[]
        for r in data:
                rate_list.append(r.rate)

        rate_list.sort()
        rate_list.reverse()

        for i in rate_list:
                if len(top_movies)>2:
                 break
                data2 = Movies.objects.get(rate = i)
                top_movies.append(data2)
      
      

        for i in mov:
                top_city.append([i.rate,i.mname])    

        
        top_city.sort()
        top_city.reverse()
      
     
        if 'user_id' in request.session.keys():
                user = Users.objects.get(id=request.session['user_id'])
                userlist.append(user)   
               
        result = {
                'users': userlist,
                'movies': data,
                'rate': top_movies,
                'city':selected_city,
                'city_movie':mov,
                'rate_city':top_city
        }      
        return render(request,'user_side/Home.html',result)

def movies(request):
        userlist=[]
        if 'user_id' in request.session.keys():
                user = Users.objects.get(id=request.session['user_id'])
                userlist.append(user)   
                
               
        selected_city=""
        mov=[]
        data = Movies.objects.all()        
        if request.method == "POST":
                
              
                selected_city=request.POST['city'] 
                for i in data:
                
                        if selected_city in i.city :
                                
                                mov.append(i)
                                request.session['city']=selected_city

        result = {
        'users': userlist,
        'movies': data,
        'city':selected_city,
        'city_movie': mov,
        }
        return render(request,'user_side/Movies.html',result)


def User_Login(request):
        if request.POST:
                email = request.POST['uemail']
                password = request.POST['password']
                data = Users.objects.all()
                for res in data:
                        if email in res.Email:
                                if password==res.password:
                                        request.session['user_id']=res.id
                                        return redirect(index)
                                else:
                                        return redirect(User_Login)  
                        else:
                                return redirect(User_Login)                      
        return render(request,'user_side/User_Login.html')

def User_Logout(request):
          if 'user_id' in request.session.keys():
               del request.session['user_id']
               return redirect(index)
          
          else:
                  return redirect(User_Login)
        
def User_Registration(request):

        if request.POST:
                name = request.POST['uname']
                email = request.POST['uemail']
                city = request.POST['city']
                password = request.POST['pass']
                com_password = request.POST['cpass']
                contact = int(request.POST['contact'])
                
                if password ==com_password:
                        data = Users(Name=name,Email=email,city=city,password=password,contact=contact)
                        data.save()
                        return redirect(User_Login)
        return render(request,'user_side/User_Registration.html')

def Book_show(request,id):
        if 'user_id' in request.session.keys():
                movie_data = Movies.objects.get(id=id)
                movie_list = [movie_data]

                print(movie_list)

                theatre_data = Theatre.objects.filter(city=request.session['city'])
                theatre_list=[]

                for i in theatre_data:
                        theatre_list.append(i)

                print(theatre_list)
        

                show_data = Show_available.objects.filter(movie=movie_data,date=date.today())
                show_list = []
                for i in show_data:
                       
                        if i.Name in theatre_list:
                                show_list.append(i)

                print(show_list)

                result = {
                        
                       'movies':movie_list,
                       'shows':show_list,
                       'theatres':theatre_list

                }
                return render(request,'user_side/Show_time.html',result)
        
        else:
                return redirect(User_Login)

def Book_show_tom(request,id):
           if 'user_id' in request.session.keys():
                movie_data = Movies.objects.get(id=id)
                movie_list = [movie_data]

                print(movie_list)

                theatre_data = Theatre.objects.filter(city=request.session['city'])
                theatre_list=[]

                for i in theatre_data:
                        theatre_list.append(i)

                print(theatre_list)
        
                tommorrow = date.today()+timedelta(1)
                print(tommorrow)
                show_data = Show_available.objects.filter(movie=movie_data,date=tommorrow)
                show_list = []
               
                for i in show_data:
                        if i.Name in theatre_list:
                                show_list.append(i)

                print(show_list)

                result = {
                        
                       'movies':movie_list,
                       'shows':show_list,
                       'theatres':theatre_list

                }
                return render(request,'user_side/Show_time_tom.html',result)
        
           else:
                return redirect(User_Login)

def Ticket_No(request,id):
         if 'user_id' in request.session.keys():
                 if request.POST:
                         No_ticket = request.POST['nt'] 
                         show_data = Show_available.objects.get(id=id)
                         result = {
                                'No_ticket':No_ticket,
                                'show_data':show_data

                                 }
                         return render(request,'user_side/theatre/'+str(show_data.Name)+'/screen'+str(show_data.screen)+'.html',result)
                       
                 return render(request,'user_side/Ticket_selection.html')
        
         else:
                 return redirect(User_Login)

def seat_selection(request):
        if 'user_id' in request.session.keys():
                 if request.GET:
                        seat = request.GET['s']
                        No_ticket = int(request.GET['no'])
                        id = request.GET['id']
                
                        show_data = Show_available.objects.get(id=id)
                        show_list = [show_data]
                       
                        total = int(show_data.price)*No_ticket
                      
                        result={

                                'No_ticket':No_ticket,
                                'Seat':seat,
                                'total':total,
                                'show_data':show_list

                        }

                        return render(request,'user_side/payment_interface.html',result)               
                 
                
        
        else:
                 return redirect(User_Login)

def payment(request):
       if 'user_id' in request.session.keys():
               if request.GET:
                       No_ticket=request.GET['No_ticket']
                       seat=request.GET['Seat']
                       total=request.GET['total']
                       id=request.GET['show_data']
                       show_data = Show_available.objects.get(id=id)
                       show_list = [show_data]
                       user_data = Users.objects.get(id=request.session['user_id'])
                       
                       
               if request.POST:
                      data=Payment(user=user_data,show=show_data,seat=seat,ticket=No_ticket,total=total)
                      data.save()
                      result={
                              'show_list':show_list,
                              'seat':seat,
                              'ticket':No_ticket,
                              'total':total
                      }
                      return render(request,'user_side/Payment_script.html',result)
               return render(request,'user_side/Payment.html')
        
       else:    
          return redirect(User_Login)