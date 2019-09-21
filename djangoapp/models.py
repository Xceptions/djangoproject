from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )


class MyUserManager(BaseUserManager):
    def create_user(self, username, phone_num, email, date_of_birth, password=None):
        """
            Creates and saves a User with the given email and date of birth and password
        """
        if not username:
            raise ValueError("users must have a username")
        if not email:
            raise ValueError("users must have an email address")
        user = self.model(
            username = username,
            phone_num = phone_num,
            email=self.normalize_email(email),
            date_of_birth = date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_num, email, date_of_birth, password):
        """
            Creates and saves a user with the given email, date of birth and password
        """
        user = self.create_user(
            username,
            phone_num,
            email,
            password=password,
            date_of_birth = date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name = 'username',
        max_length=55,
        unique=True
    )
    phone_num = models.CharField(
        verbose_name = 'phone number',
        max_length=255,
        unique=False
    )
    email = models.EmailField(
        verbose_name = 'email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_num','email','date_of_birth']

    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        # is used to find out if the user has a specific type of permission
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
    def get_short_name(self):
        return self.email