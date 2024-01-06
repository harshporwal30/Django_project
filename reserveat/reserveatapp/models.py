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
    owner_id= models.ForeignKey(resadmin, on_delete= models.CASCADE)
    res_name= models.CharField(max_length= 200)
    res_address= models.CharField(max_length= 500)
    res_contact= models.BigIntegerField()
    class meta:
        db_table= 'restaurants'

class tables(models.Model):
    res_id= models.ForeignKey(restaurant, on_delete= models.CASCADE)
    tablen0= models.IntegerField()
    seating_capacity= models.IntegerField()
    booking_status= models.BooleanField(default= False)
    class meta:
        db_table= 'tables'