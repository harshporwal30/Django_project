from django.db import models

# Create your models here.
class regadmin(models.Model):
    firstname= models.CharField(max_length= 200)
    lastname= models.CharField(max_length= 200)
    email= models.EmailField(max_length= 200)
    phoneno= models.BigIntegerField()
    password= models.CharField(max_length= 250)

    class meta:
        db_table= 'admin-login'

