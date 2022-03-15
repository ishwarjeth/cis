from turtle import back
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import *
from django.contrib.auth.models import PermissionsMixin



# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    first_name      = models.CharField(max_length=50,verbose_name="First Name",blank=True,null=True)
    last_name       = models.CharField(max_length=50,verbose_name="Last Name",blank=True,null=True)
    username        = models.CharField(max_length=50,verbose_name="username",blank=True,null=True)
    email           = models.EmailField(('email address'),unique=True,blank=True,null=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(('active'), default=True)
    is_verified     = models.BooleanField(default=False)
    objects         = CustomUserManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.first_name +" "+ self.last_name
    def __str__(self) -> str:
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=50,verbose_name="Category",blank=True,null=True,unique=True)
    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    p_name = models.CharField(max_length=200,verbose_name="Product Name",blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price",blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    p_discription = models.TextField()
    timestamp = models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.p_name
    class Meta:
        ordering = ["-timestamp"]

class ImageList(models.Model):
    img = models.URLField(blank=True,null=True)
    def __str__(self) -> str:
        return self.img
