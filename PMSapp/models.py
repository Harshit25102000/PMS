from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

# User customization goes down

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_employee = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def __str__(self):
        return self.email


class entries(models.Model):
    entry_id= models.AutoField
    employee_id= models.CharField(max_length=100,unique=True)
    First_name = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100,null=True, blank=True)
    Last_name = models.CharField(max_length=100,null=True, blank=True)
    Department = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    Email_id = models.CharField(max_length=200,unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    joining_date = models.CharField(max_length=20)
    Reporting_manager= models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.First_name)



class manager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=100,unique=True)
    First_name = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100, null=True, blank=True)
    Last_name = models.CharField(max_length=100, null=True, blank=True)
    Email_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.First_name)

class employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    assigned_manager = models.ForeignKey(manager, on_delete=models.CASCADE)
    progress=models.IntegerField(default=0)
    employee_id = models.CharField(max_length=100,unique=True)
    First_name = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100, null=True, blank=True)
    Last_name = models.CharField(max_length=100, null=True, blank=True)
    Department = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    Email_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    joining_date = models.CharField(max_length=20)
    Reporting_manager = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.First_name)

class adminuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=100,unique=True)
    First_name = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100, null=True, blank=True)
    Last_name = models.CharField(max_length=100, null=True, blank=True)
    Email_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.First_name)

class reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=500, default="Not Mentioned")
    date = models.DateField()
    time = models.TimeField()
    is_frozen = models.BooleanField(default=False)
    freezing_time=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.subject)

class comments(models.Model):
    review = models.ForeignKey(reviews,on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    message = models.CharField(max_length=5000,null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.sender)


class self_appraisals(models.Model):

    created_by= models.ForeignKey(employee, on_delete=models.CASCADE)
    handled_by= models.ForeignKey(manager, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status=models.CharField(max_length=100,default="Pending")
    application = models.CharField(max_length=50000,default="Empty...")

    def __str__(self):
        return str(self.created_by)
