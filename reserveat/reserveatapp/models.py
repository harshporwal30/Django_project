from django.db import models

# Create your models here.
class resadmin(models.Model):
    firstname= models.CharField(max_length= 200)
    lastname= models.CharField(max_length= 200)
    email= models.EmailField(max_length= 200)
    phoneno= models.BigIntegerField()
    password= models.CharField(max_length= 250)
    class meta:
        db_table= 'admin-login'

class restaurant(models.Model):
    ownerid= models.ForeignKey(resadmin, on_delete= models.CASCADE)
    res_name= models.CharField(max_length= 200)
    res_address= models.CharField(max_length= 500)
    res_contact= models.BigIntegerField()
    class meta:
        db_table= 'restaurants'

class tables(models.Model):
    res_id= models.ForeignKey(restaurant, on_delete= models.CASCADE)
    tablename= models.CharField(max_length= 200, default= '')
    tableno= models.IntegerField()
    seating_capacity= models.IntegerField()
    table_location= models.CharField(max_length=200, default="" )
    booking_status= models.BooleanField(default= False)
    available= models.BooleanField(default= True)
    class meta:
        db_table= 'tables'

class ambianceimg(models.Model):
    image= models.ImageField(upload_to='media')
    resid= models.ForeignKey(restaurant, on_delete= models.CASCADE)
    class meta:
        db_table= "ambiance"

class users(models.Model):
    first_name= models.CharField(max_length= 200)
    last_name= models.CharField(max_length= 200)
    email= models.EmailField()
    phoneno= models.BigIntegerField()
    address= models.TextField(max_length= 500)
    password= models.CharField(max_length= 250)
    class meta:
        db_table= 'users'

class bookings(models.Model):
    restaurantid= models.ForeignKey(restaurant, on_delete= models.CASCADE)
    tableid= models.ForeignKey(tables, on_delete= models.CASCADE)
    customerid= models.ForeignKey(users, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now= True)
    booked_for= models.DateField()
    booking_time= models.TimeField()
    class meta:
        db_table= 'bookings'