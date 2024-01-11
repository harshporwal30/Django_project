from django.shortcuts import render, redirect
from .models import resadmin, restaurant, ambianceimg
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
        userobj = resadmin.objects.get(email=usersession)
        resobj = restaurant.objects.filter(ownerid_id=userobj.id)

        if resobj:
            robj = restaurant.objects.get(ownerid_id=userobj.id)
            return render(request, 'dashboard.html', {'user': userobj, 'restaurant': robj})
        else:
            message = "Oops! You haven't registered any restaurant yet. Please register a restaurant with us."
            return render(request, 'dashboard.html', {'user': userobj, 'message': message})

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
            userobj = resadmin.objects.get(email=usersession)
            return render(request, 'ambianceform.html',{'user': userobj})
        elif request.method == "POST":
            usersession = request.session['admin']
            userobj = resadmin.objects.get(email=usersession)
            print(userobj.id)
            resobj= restaurant.objects.get(ownerid_id=userobj.id)
            print(resobj.id)
            image_file= request.FILES.get('ambiance')
            print(image_file)
            print(request.FILES)
            if resobj:
                if image_file:
                    ambobj= ambianceimg(image=image_file, resid=resobj)
                    ambobj.save()
                    return redirect('../reg-table/')
                else:
                    return HttpResponse("sorry")
            else:
                return HttpResponse("restaurant does not exits")

def addtables(request):
    usersession = request.session['admin']
    userobj = resadmin.objects.get(email=usersession)
    resobj= restaurant.objects.get(ownerid_id=userobj.id)
    
    return render(request, 'tabelreg-form.html',{'user': userobj, 'restaurant': resobj})


