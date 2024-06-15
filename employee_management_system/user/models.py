from django.db import models

# Create your models here.

class Organization(models.Model):
    org_id = models.BigAutoField(primary_key=True)
    org_name = models.CharField(max_length=255,blank=False,null=True)
    
    class Meta:
        managed = True
        db_table = 'organization'
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20,blank=False,null=True)
    password = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)
    active = models.IntegerField(default=1,blank=False,null=False)

    class Meta:
        managed = True
        db_table = 'user'

class UserDetails(models.Model):
    user_dtls_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='user1',on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, default=1,related_name='organization1',on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,blank=False,null=True)
    lastname = models.CharField(max_length=50,blank=False,null=True)
    email = models.CharField(max_length=100,blank=False,null=True)
    phone = models.CharField(max_length=20,blank=False,null=True)
    user_role = models.IntegerField(blank=False,null=True)
    profile_pic = models.CharField(max_length=255,blank=False,null=True)
    designation = models.CharField(max_length=255,blank=False,null=True)
    salary = models.BigIntegerField(blank=False,null=True)
    joining_date = models.DateField(blank=False,null=True)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)

    class Meta:
        managed = True
        db_table = 'user_details'
        

    

    