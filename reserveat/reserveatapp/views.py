from django.shortcuts import render, redirect
from .models import resadmin, restaurant, ambianceimg,tables, bookings, users
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView
from django.utils import timezone

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
            {'start_time': '12:00', 'end_time': '14:00'},
            {'start_time': '22:00', 'end_time': '23:45'},
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
        tableobj.booking_status= "Confirmed"
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
            {'start_time': '12:00', 'end_time': '14:00'},
            {'start_time': '22:00', 'end_time': '23:45'},
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
    usersession = request.session['admin']
    adminobj = resadmin.objects.get(email=usersession)
    resobj= restaurant.objects.get(ownerid_id=adminobj.id)
    ambianceimage= ambianceimg.objects.filter(resid_id= resobj.id)
    return render(request, 'settings.html', {'user': adminobj, 'restaurant': resobj, 'ambiance': ambianceimage})


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
    


class rstrnt(ListView):
    model= restaurant, ambianceimg
    template_name= "index.html"
    context_object_name= "resobj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user' in self.request.session:
            data = self.request.session['user']
            user = users.objects.get(email=data)
            context['session'] = user
            return context
        else:
            error_message = "Unauthorized Access."
            return {'msg': error_message}

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
        


