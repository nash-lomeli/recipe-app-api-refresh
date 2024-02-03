import jwt
import uuid

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

from drc.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        print('AUTHENTICATION class UserManager(BaseUserManager):')

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(max_length=255, unique=True,db_index=True)
    email = models.EmailField(max_length=255,db_index=True,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    print('AUTHENTICATION MODELS CLASS USER')

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their email instead.
        """
        return self.email

    def get_short_name(self):
        print('get_short_name(self):')
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.email

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        #return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])#token.decode('utf-8')
        return token
