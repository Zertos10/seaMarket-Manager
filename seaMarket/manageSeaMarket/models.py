from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
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
        user.set_password(password)
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
    def has_perm(self,perm,obj=None):
        return self.isAdmin
    def has_module_perms(self,app_label):
        # Check if user has permission to view the app 'app_label'
        return True
    @property
    def is_staff(self):
        return self.isAdmin
class Product(models.Model):
    productId = models.IntegerField(unique=True)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    percentSale = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    sellArticle = models.IntegerField()
    comments = models.TextField()
    class Meta:
        ordering = ['productId']
        verbose_name = 'Product'
class Category(models.Model):
    nameCategory = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    class Meta:
        ordering = ['nameCategory']
        verbose_name = 'Category'
class History(models.Model):
    addDate = models.DateTimeField()
    typeHistory = models.CharField(max_length=100)
    valueHistory = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product)
    class Meta:
        ordering = ['addDate','typeHistory','valueHistory']
        verbose_name = 'History'