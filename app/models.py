from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.safestring import mark_safe
import datetime, uuid

# Create your models here.

ITEMS = (
  ("Electronics","Electronics"),
  ("Cables","Cables"),
  ("Accessories","Accessories"),
)

ROOMS = (
  ("IT", "IT"),
  ("DKV","DKV")
)

STATUS_CHOICES = (
  ('Diterima', 'Diterima'),
  ('Diproses', 'Diproses'),
  ('Dikembalikan', 'Dikembalikan')
)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phonenumber = PhoneNumberField()
    date_joined = models.DateTimeField(default=datetime.datetime.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # Specify unique related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='client_set',
        related_query_name='client',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='client_set',
        related_query_name='client',
    )

    def __str__(self):
       return self.username

    class Meta:
        verbose_name = "Akun"
        verbose_name_plural = "Akun"

class Barang(models.Model):
  id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False, max_length=36)
  name = models.CharField(max_length=100, null=True)
  category = models.CharField(max_length=100, choices=ITEMS, null=True)
  quantity = models.PositiveIntegerField(null=True)
  room = models.CharField(max_length=100, choices=ROOMS, null=True)
  image = models.ImageField(null=True,blank=True)

  def item(self):
     return mark_safe("<img src='{}' width='100px' height='100px'>".format(self.image.url))
  
  
  def __str__(self):
    return f"{self.name}"
  
  class Meta:
     verbose_name="Barang"
     verbose_name_plural = "Barang"
  
class Peminjaman(models.Model):
  id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False, max_length=36)
  item_code = models.CharField(editable=False, max_length=36)
  client = models.ForeignKey(Account,on_delete=models.CASCADE,max_length=255,editable=False)
  item = models.ForeignKey(Barang, on_delete=models.CASCADE, null=True, editable=False)
  room = models.CharField(max_length=100,choices=ROOMS,null=True, editable=False)
  category = models.CharField(max_length=100,choices=ITEMS,null=True, editable=False)
  lending_quantity = models.PositiveIntegerField(null=True, editable=False)
  description = models.TextField(null=True)
  date_lending = models.DateTimeField(default=datetime.datetime.now,editable=False)
  return_time = models.DateTimeField(null=True, blank=True, editable=False)
  status = models.CharField(max_length=50,choices=STATUS_CHOICES,null=True)

  class Meta:
     verbose_name = "Peminjaman"
     verbose_name_plural = "Peminjaman"