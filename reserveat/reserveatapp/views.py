from django.shortcuts import render, redirect
from .models import resadmin, restaurant, ambianceimg,tables, bookings, users
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse
from django.http import QueryDict
import string
import random
from datetime import datetime

# Create your views here.
def reg(request):
    if request.method == "GET":
        return render(request, 'adminreg.html')

    elif request.method == "POST":
        fn= request.POST['firstname']
        ln= request.POST['lastname']
        email= request.POST['email']
        phone= request.POST['telephoneno']
        pswd= request.POST['password']
        pwd= make_password(pswd)
        adminobj= resadmin(firstname=fn, lastname=ln,email=email,phoneno=phone,password=pwd)
        adminobj.save()
        success_message = "Registered successfully! You can now log in."
        return render(request, 'adminreg.html', {'success_message': success_message})
    
def adminlogin(request):
    if request.method == "GET":
        return render (request, 'adminlogin.html')
    elif request.method == "POST":
        adt= resadmin.objects.filter(email= request.POST.get('username'))
        if adt:
            adtobj= resadmin.objects.get(email= request.POST.get('username'))
            passf= request.POST.get('password')
            flag= check_password(passf, adtobj.password)

            if flag:
                request.session['admin']= request.POST.get('username')
                return redirect('../dashboard/')
            else:
                 error_message ="Wrong username or password"
                 return render(request, 'adminlogin.html', {'msg': error_message})
        else:
            error_message ="No user found."
            return render(request, 'adminlogin.html', {'msg': error_message})

def logout(request):
    if 'admin' in request.session:
        del request.session['admin']
        return redirect('../adlogin/')
    elif 'user' in request.session:
        del request.session['user']
        return redirect('../login/')
    
def dashboard(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj = restaurant.objects.filter(ownerid_id=adminobj.id)
        if resobj:
            
            robj = restaurant.objects.get(ownerid_id=adminobj.id)
            tableobj= tables.objects.filter(res_id_id=robj)
            time_slots = [
            {'start_time': '09:00', 'end_time': '11:00'},
            {'start_time': '11:00', 'end_time': '13:00'},
            {'start_time': '13:00', 'end_time': '15:00'},
            {'start_time': '15:00', 'end_time': '17:00'},
            {'start_time': '17:00', 'end_time': '19:00'},
            {'start_time': '19:00', 'end_time': '21:00'},
            {'start_time': '21:00', 'end_time': '22:00'}
        ]
            return render(request, 'dashboard.html', {'user': adminobj, 'restaurant': robj, "table": tableobj, 'time_slots':time_slots})
        else:
            message = "Oops! You haven't registered any restaurant yet. Please register a restaurant with us."
            return render(request, 'dashboard.html', {'user': adminobj, 'message': message})

    else:
        error_message ="Unauthorized Access."
        return render(request, 'dashboard.html', {'msg': error_message})
    
def addrestaurant(request):
    if request.method == "POST":
        userid= request.session['admin']
        aobj= resadmin.objects.get(email= userid)
        name= request.POST['new_name']
        address= request.POST['new_address']
        contact= request.POST['telephoneno']
        restaurantobj= restaurant(res_name= name, res_address= address, res_contact= contact, ownerid_id= aobj.id)
        restaurantobj.save()
        return redirect('../add-ambiance/')
    
def addambiance(request):
    if 'admin' in request.session:
        if request.method == "GET":
            usersession = request.session['admin']
            adminobj = resadmin.objects.get(email=usersession)
            resobj= restaurant.objects.get(ownerid_id=adminobj.id)
            return render(request, 'ambianceform.html',{'user': adminobj, 'restaurant': resobj})
        elif request.method == "POST":
            usersession = request.session['admin']
            adminobj = resadmin.objects.get(email=usersession)
            print(adminobj.id)
            resobj= restaurant.objects.get(ownerid_id=adminobj.id)
            print(resobj.id)
            image_file= request.FILES.get('ambiance')
            print(image_file)
            print(request.FILES)
            flag = False
            if resobj:
                if image_file:
                    flag = True
                    resobj.res_display= image_file
                    resobj.save()
                    return render(request, 'ambianceform.html', {'flag': flag, 'user': adminobj, 'restaurant': resobj})
                else:
                    return HttpResponse("sorry")
            else:
                return HttpResponse("restaurant does not exits")

def addtables(request):
    if request.method=="POST":
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        tn= request.POST.get('tableNumber')
        sc= request.POST.get('seatingCapacity')
        lc= request.POST.get('location')
        tnme= request.POST.get('tableName')
        tableobj= tables(tableno= tn, seating_capacity= sc, tablename= tnme, table_location= lc, res_id_id= resobj.id)
        tableobj.save()
        return redirect('../dashboard/')


def rtables(request):
    if request.method== "POST":
        flag= True
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        return render(request, 'ambianceform.html', {'flag': flag, 'user': adminobj, 'restaurant': resobj})

        
def tablelog(request):
    if 'admin' in request.session:
        if request.method== "GET":
            usersession = request.session['admin']
            adminobj = resadmin.objects.get(email=usersession)
            resobj= restaurant.objects.get(ownerid_id=adminobj.id)
            tableobj= tables.objects.filter(res_id_id=resobj)
            return render(request, 'tablelogistics.html',{'table': tableobj, 'user': adminobj})
    else:
        error_message ="Unauthorized Access."
        return render(request, 'tablelogistics.html',{'msg': error_message})
    
def reserve(request):
    if request.method=="POST":
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        cname= request.POST.get('customerName')
        cemail= request.POST.get('customeremail')
        rdate= request.POST.get('date')
        rtime= request.POST.get('time')
        tno= request.POST.get('table')
        start_time_str, end_time_str = rtime.split('-')

        tableobj= tables.objects.get(res_id_id=resobj, tableno= tno)
        cobj= users.objects.get(email= cemail)
        bookingobj= bookings(restaurantid= resobj, tableid= tableobj, customerid= cobj, booking_date= rdate, start_time= start_time_str, end_time= end_time_str)
        tableobj.booking_status= "Booked"
        tableobj.available= False
        bookingobj.save()
        tableobj.save()
        return HttpResponse("Test")
    
def managetable(request, id):
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        tableobj= tables.objects.get(id= id)
        return render(request, 'tablelogistics.html',{'etable': tableobj, 'user': adminobj})

def update(request, id):
    if request.method == "POST":
        tableobj= tables.objects.get(id= id)
        tableobj.tableno= request.POST.get('tableNumber')
        tableobj.seating_capacity= request.POST.get('seatingCapacity')
        tableobj.table_location= request.POST.get('location')
        tableobj.tablename= request.POST.get('tableName')
        a= request.POST.get('selection')
        if a == "Yes":
            tableobj.available = True
        elif a == "No":
            tableobj.available= False
        tableobj.save()
        return redirect('../tables/')
    

def reservationadm(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        time_slots = [
            {'start_time': '09:00', 'end_time': '11:00'},
            {'start_time': '11:00', 'end_time': '13:00'},
            {'start_time': '13:00', 'end_time': '15:00'},
            {'start_time': '15:00', 'end_time': '17:00'},
            {'start_time': '17:00', 'end_time': '19:00'},
            {'start_time': '19:00', 'end_time': '21:00'},
            {'start_time': '21:00', 'end_time': '22:00'}
        ]

        selected_time_slot = request.POST.get('time_slot')

        print(selected_time_slot)
        if selected_time_slot:
            start_time, end_time = selected_time_slot.split('-')
            bookingobj = bookings.objects.filter(restaurantid=resobj, start_time__gte=start_time, end_time__lte=end_time)
        else:
            
            bookingobj = bookings.objects.filter(restaurantid=resobj)

        return render(request, 'reservation-administration.html', {'booking': bookingobj, 'user': adminobj, 'time_slots': time_slots})
    else:
        error_message = "Unauthorized Access."
        return render(request, 'tablelogistics.html', {'msg': error_message})



def updatres(request, id):
    if request.method == "POST":
        userid= request.session['admin']
        resobj= restaurant.objects.get(id=id)
        resobj.res_name= request.POST['new_name']
        resobj.res_address= request.POST['new_address']
        resobj.res_contact= request.POST['telephoneno']
        resobj.res_description= request.POST['des']
        resobj.save()
        return redirect('../settings/')
    

def settings(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        return render(request, 'settings.html', {'user': adminobj, 'restaurant': resobj})
    else:
        error_message ="Unauthorized Access."
        return render(request, 'tablelogistics.html',{'msg': error_message})

def otamb(request):
    if request.method == "POST":
            usersession = request.session['admin']
            adminobj = resadmin.objects.get(email=usersession)
           
            resobj= restaurant.objects.get(ownerid_id=adminobj.id)
            
            image_file= request.FILES.get('ambiance')
            if resobj:
                if image_file:
                    flag = True
                    amb= ambianceimg(image=image_file, resid_id= resobj.id)
                    amb.save()
                    return render(request, 'settings.html', {'flag': flag, 'user': adminobj, 'restaurant': resobj})
                
def viewgallery(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        ambianceimage= ambianceimg.objects.filter(resid_id= resobj.id)
        return render(request, 'settings.html', {'user': adminobj,'gallery': ambianceimage})
    else:
        error_message ="Unauthorized Access."
        return render(request, 'tablelogistics.html',{'msg': error_message})
    

def deleteimg(request, id):
    if request.method == "POST":
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        
        ambianceimge= ambianceimg.objects.get(id=id)
        ambianceimge.delete()
        
        return redirect("../../viewgallery/")


#user end views

def registration(request):
    if request.method == "GET":
        return render(request, 'registration.html')
    elif request.method == "POST":
        fn= request.POST['firstname']
        ln= request.POST['lastname']
        email= request.POST['email']
        phone= request.POST['telephoneno']
        pswd= request.POST['password']
        pwd= make_password(pswd)
        adrs= request.POST['address']
        userobj= users(first_name=fn, last_name=ln,email=email,phoneno=phone,password=pwd, address= adrs)
        userobj.save()
        success_message = "Registered successfully! You can now log in."
        return render(request, 'registration.html', {'success_message': success_message})
    




def rstrnt(request):
    if 'user' in request.session:
        userobj= request.session['user']
        cobj= users.objects.get(email=userobj)
        resobj= restaurant.objects.all()
        return render(request, 'index.html', {'resobj': resobj, 'user': cobj})
    else:
        error_message = "Unauthorized Access."
        return render (request, 'index.html',{'msg': error_message})


def login(request):
    if request.method == "GET":
        return render (request, 'login.html')
    elif request.method == "POST":
        usr= users.objects.filter(email= request.POST.get('username'))
        if usr:
            usrobj= users.objects.get(email= request.POST.get('username'))
            passf= request.POST.get('password')
            flag= check_password(passf, usrobj.password)

            if flag:
                request.session['user']= request.POST.get('username')
                return redirect('../index/')
            else:
                 error_message ="Wrong username or password"
                 return render(request, 'login.html', {'msg': error_message})
        else:
            error_message ="No user found."
            return render(request, 'login.html', {'msg': error_message})
        


def details(request, id):
    if 'user' in request.session:
        userobj= request.session['user']
        cobj= users.objects.get(email=userobj)
        resobj= restaurant.objects.get(id=id)
        tableobj= tables.objects.filter(res_id_id=resobj.id)
        ambobj= ambianceimg.objects.filter(resid_id=resobj.id)
        time_slots = [
            {'start_time': '09:00', 'end_time': '11:00'},
            {'start_time': '11:00', 'end_time': '13:00'},
            {'start_time': '13:00', 'end_time': '15:00'},
            {'start_time': '15:00', 'end_time': '17:00'},
            {'start_time': '17:00', 'end_time': '19:00'},
            {'start_time': '19:00', 'end_time': '21:00'},
            {'start_time': '21:00', 'end_time': '22:00'}
        ]
        error_message = request.GET.get('error_message', None)
        return render(request, 'booking page.html', {'msgs': error_message,'resobj': resobj, 'user': cobj,'tables':tableobj, 'time_slots': time_slots, 'ambiance': ambobj})
    else:
            error_message = "Unauthorized Access."
            return {'msg': error_message}
    

def check(request, id):
    if request.method == "POST":
        
        if 'user' in request.session:
            userobj= request.session['user']
            cobj= users.objects.get(email=userobj)

            table_obj = tables.objects.get(id=id)
            resid= table_obj.res_id.id
            resobj= restaurant.objects.get(id= resid)
            bookings_list = bookings.objects.filter(tableid_id=table_obj)
            tdate= request.POST.get('date')
            selected_time_slot = request.POST.get('time_slot')
            start_time, end_time = selected_time_slot.split('-')

            
            if bookings_list.filter(start_time=start_time, booking_date=tdate, booking_status = "Confirmed").exists():
                error_message ="Table Not Available for Seletcted Time Slot"
                return redirect(reverse('viewdetails', args=[resid]) + f'?error_message={error_message}')
            else:
                return render(request, 'booking form.html', { 'user': cobj, 'table': table_obj,'resobj':resobj ,'time_slot': selected_time_slot})

def book(request):
    if request.method== "POST":
        userobj= request.session['user']
        cobj= users.objects.get(email=userobj)
        rname= request.POST['restaurant']
        rdate= request.POST['booking-date']
        rtime= request.POST['time']
        rguess= request.POST.get('guests')
        rtable= request.POST.get('table')
        start_time, end_time= rtime.split("-")
        bookingobj= bookings(restaurantid_id= rname, tableid_id= rtable,customerid_id= cobj.id, booking_date= rdate, start_time= start_time, end_time= end_time, booking_status= "Pending" )
        bookingobj.save()
        string.ascii_letters=  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        a= random.choice(string.ascii_letters)
        bid1=  a + str(cobj.id) + str(rdate) 
        bid= bid1.replace('-', '')
        bookingobj.bookingid= bid
        bookingobj.save()
        book1= bookings.objects.get(bookingid= bid)
        tableobj= tables.objects.get(id= rtable)
        tableobj.booking_status= "Pending"
        tableobj.save()
        table1= tables.objects.get(id= rtable)

        return render (request, 'summary.html', {'booking': book1, 'user': cobj, 'tableobj': table1})
    
def summary(request, bid):
    userobj= request.session['user']
    cobj= users.objects.get(email=userobj)
    new_booking= bookings.objects.get(bookingid= bid)
    print(new_booking.bookingid)
    table1= tables.objects.get(id= new_booking.tableid_id)
    return render (request, 'summary.html', {'booking': new_booking, 'user': cobj, 'tableobj': table1})

def profile(request):
    userobj= request.session['user']
    cobj= users.objects.get(email=userobj)
    booking= bookings.objects.filter(customerid_id= cobj.id)
    return render(request, 'profile.html',{'user': cobj, 'booking': booking})

def cancelbooking(request):
    if request.method== "POST":
        userobj= request.session['user']
        cobj= users.objects.get(email=userobj)
        booking= bookings.objects.filter(customerid_id= cobj.id)
        a= request.POST.get('booking_id')
        bkobj= bookings.objects.get(id=a)

        tbl= tables.objects.get(id= bkobj.tableid.id)
        print(tbl)
        tbl.booking_status = "Not Booked"
        tbl.save()
        bookingobj= bookings.objects.get(id= a)
        bookingobj.booking_status= "Cancelled"
        bookingobj.save()
        url= reverse('profile')
        return redirect(url)
    

def paymentsuccess(request, tid, orderid):
    userobj= request.session['user']
    cobj= users.objects.get(email=userobj)
    booking= bookings.objects.filter(customerid_id= cobj.id)
    bkobj= bookings.objects.get(bookingid= orderid)
    bkobj.booking_status= "Confirmed"
    bkobj.transaction_id= tid
    bkobj.save()
    tbl= tables.objects.get(id= bkobj.tableid.id)
    tbl.booking_status= "Booked"
    tbl.save()
    return render(request, 'paymentsuccess.html', {'bk': bkobj, 'user': cobj, 'booking': booking})