import hashlib
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.hashers import make_password
from django.db.models.signals import m2m_changed

import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,lastName=None,firstName=None,password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email), 
            lastName=lastName,
            firstName=firstName
            )
        md5_password = hashlib.md5(password.encode()).hexdigest()
        user.set_password(md5_password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password):
        user = self.create_user(
            email,
            password=password
        )
        user.isAdmin = True
        user.save(using=self._db)
        return user
    

# Register your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=100)
    firstName = models.CharField(max_length=100,blank=True,null=True)
    lastName = models.CharField(max_length=100,blank=True,null=True)
    isAdmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    def has_perm(self,perm=None,obj=None):
        return self.isAdmin
    def has_module_perms(self,app_label):
        # Check if user has permission to view the app 'app_label'
        return True
    def set_password(self,raw_password):
        md5_password = hashlib.md5(raw_password.encode())
        self.password = md5_password.hexdigest()
    @property
    def is_staff(self):
        return self.isAdmin
class Product(models.Model):
    productId = models.IntegerField(unique=True)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    percentSale = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    quantity = models.IntegerField(default=0)
    sellArticle = models.IntegerField(default=0)
    comments = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ['productId']
        verbose_name = 'Product'
@receiver(post_save, sender=Product)
def _post_save_receiver(sender,instance,created, **kwargs):
    if created:
        all_category, _ = Category.objects.get_or_create(nameCategory="all")
        instance.category_set.add(all_category)
    pass

class Category(models.Model):
    nameCategory = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    class Meta:
        ordering = ['nameCategory']
        verbose_name = 'Category'

@receiver(m2m_changed, sender=Product.category_set.through)
def add_all_category(sender, instance, action, **kwargs):
    if action == "post_add":
        all_category, created = Category.objects.get_or_create(nameCategory="all")
        if all_category not in instance.category_set.all():
            instance.category_set.add(all_category)
class History(models.Model):
    typeHistory = models.CharField(max_length=100)
    valueHistory = models.DecimalField(max_digits=10, decimal_places=2)
    quantityHistory = models.IntegerField(default=0)
    addDate = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    class Meta:
        ordering = ['addDate','typeHistory','valueHistory','quantityHistory']
        verbose_name = 'History'