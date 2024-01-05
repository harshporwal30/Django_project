from django.shortcuts import render, redirect
from .models import regadmin
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
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
        adminobj= regadmin(firstname=fn, lastname=ln,email=email,phoneno=phone,password=pwd)
        adminobj.save()
        success_message = "Registered successfully! You can now log in."
        return render(request, 'adminreg.html', {'success_message': success_message})
    
def adminlogin(request):
    if request.method == "GET":
        return render (request, 'adminlogin.html')
    elif request.method == "POST":
        adt= regadmin.objects.filter(email= request.POST.get('username'))
        if adt:
            adtobj= regadmin.objects.get(email= request.POST.get('username'))
            passf= request.POST.get('password')
            flag= check_password(passf, adtobj.password)

            if flag:
                request.session['admin']= request.POST.get('username')
                session= request.session['admin']
                return redirect('../manage/')
            else:
                return HttpResponse("Wrong username or password")

def manageres(request):
    return render(request, 'managerestaurant.html', {'user': request.session['admin']})