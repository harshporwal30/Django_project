from django.shortcuts import render, redirect
from .models import resadmin, restaurant
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.contrib import messages
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
                return redirect('../manage/')
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
    
from django.shortcuts import render
from .models import resadmin, restaurant

def manageres(request):
    if 'admin' in request.session:
        usersession = request.session['admin']
        userobj = resadmin.objects.get(email=usersession)
        resobj = restaurant.objects.filter(owner_id=userobj.id)

        if resobj:
            return render(request, 'managerestaurant.html', {'user': userobj.firstname, 'restaurant': resobj})
        else:
            message = "Oops! You haven't registered any restaurant yet. Please register a restaurant with us."
            return render(request, 'managerestaurant.html', {'user': userobj.firstname, 'message': message})

    else:
        error_message ="Unauthorized Access."
        return render(request, 'managerestaurant.html', {'msg': error_message})