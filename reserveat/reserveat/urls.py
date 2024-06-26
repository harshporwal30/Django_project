"""
URL configuration for reserveat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reserveatapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', views.reg, name='adminreg'),
    path('admin-login/', views.adminlogin, name='adminlogin'),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('logout/', views.logout, name= "logout"),
    path('add/', views.addrestaurant, name="create"),
    path('add-ambiance/', views.addambiance, name="upld"),
    path('addambiance/', views.otamb, name='otamb'),
    path('reg-table/', views.addtables, name="regtable"),
    path('tables/', views.tablelog, name="tables"),
    path('add-table/', views.rtables, name="addtable"),
    path('resvere/', views.reserve, name="addreservation"),
    path('manage-table/<int:id>/', views.managetable, name="managetable"),
    path('update/<int:id>', views.update, name="updttable"),
    path('administration/', views.reservationadm, name="res-administration"),
    path('index/', views.rstrnt, name="index"),
    path('login/', views.login, name="login"),
    path('user-registration/', views.registration, name= 'uregister'),
    path('update-res/<int:id>',views.updatres, name="updtres" ),
    path('settings/', views.settings, name="settings"),
    path('viewgallery/', views.viewgallery),
    path('delete/<int:id>/', views.deleteimg, name="deleteimg"),
    path('details/<int:id>/', views.details, name="viewdetails"),
    path('book/<int:id>/', views.check, name="check"),
    path('book-table/', views.book, name="booktable"),
    path('summary/<str:bid>/', views.summary, name="summary"),
    path('profile/', views.profile, name="profile"),
    path('cancel-booking/', views.cancelbooking, name="cancel-booking"),
    path('paymentsucess/<str:tid>/<str:orderid>', views.paymentsuccess, name='paymentsuccess'),
    path('cancel-payment/', views.cancelpament, name="cancel-payment"),
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('filter-by-location/<str:location>/', views.locationfilter, name='paymentsuccess'),


    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)