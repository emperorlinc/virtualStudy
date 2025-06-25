from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from random import choice

# Create your models here.


def make_uid():
    uid = ''
    for _ in range(8):
        uid += str(choice(range(0, 10)))
    return uid


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("User must have an email.")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=225, blank=True, null=True)
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225, unique=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=8, blank=True, unique=True)
    profile_pic = models.ImageField(
        upload_to='static/images', blank=True, default='static/images/jjk.jpg')
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.uid = make_uid()
        return super().save(args, kwargs)

    def __str__(self) -> str:
        return self.user.name[0]


ROOM_TYPE = (
    ('g', 'group'),
    ('p', 'peer'),
)


class Faculty(models.Model):
    host = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Faculties'

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True)
    faculty = models.ForeignKey(
        to=Faculty, on_delete=models.CASCADE, blank=True, null=True)
    members = models.ManyToManyField(to=UserProfile)
    uid = models.CharField(max_length=8, unique=True, blank=True)
    room_type = models.CharField(max_length=1, choices=ROOM_TYPE, blank=True)

    def save(self, *args, **kwargs):
        self.uid = make_uid()
        return super().save(args, kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        word = self.body.split(' ')
        return f'{word[0]} {word[1]} {word[2]}...'
