from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20,blank=False,null=True)
    password = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)

    class Meta:
        managed = True
        db_table = 'user'

class UserDetails(models.Model):
    user_dtls_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='user1',on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,blank=False,null=True)
    lastname = models.CharField(max_length=50,blank=False,null=True)
    email = models.CharField(max_length=100,blank=False,null=True)
    phone = models.CharField(max_length=20,blank=False,null=True)
    user_role = models.IntegerField(blank=False,null=True)
    profile_pic = models.CharField(max_length=255,blank=False,null=True)
    active = models.IntegerField(default=1,blank=False,null=False)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)

    class Meta:
        managed = True
        db_table = 'user_details'

    