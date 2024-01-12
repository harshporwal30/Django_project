from django.shortcuts import render, redirect
from .models import resadmin, restaurant, ambianceimg,tables, bookings, users
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.forms import ModelForm

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
    
def dashboard(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj = restaurant.objects.filter(ownerid_id=adminobj.id)
        if resobj:
            
            robj = restaurant.objects.get(ownerid_id=adminobj.id)
            tableobj= tables.objects.filter(res_id_id=robj)
            return render(request, 'dashboard.html', {'user': adminobj, 'restaurant': robj, "table": tableobj})
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
                    ambobj= ambianceimg(image=image_file, resid=resobj)
                    ambobj.save()
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
    if request.method== "GET":
        usersession = request.session['admin']
        adminobj = resadmin.objects.get(email=usersession)
        resobj= restaurant.objects.get(ownerid_id=adminobj.id)
        tableobj= tables.objects.filter(res_id_id=resobj)
        return render(request, 'tablelogistics.html',{'table': tableobj, 'user': adminobj})
    
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
        tableobj= tables.objects.get(res_id_id=resobj, tableno= tno)
        print(tableobj.tablename)
        cobj= users.objects.get(email= cemail)
        bookingobj= bookings(restaurantid= resobj, tableid= tableobj, customerid= cobj, booked_for= rdate, booking_time= rtime)
        bookingobj.save()
        return HttpResponse("Test")