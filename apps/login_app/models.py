from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = []

        if User.objects.filter(email=postData['email']).exists():
            errors.append('This email address is already registered')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('please enter a valid email format')

        if len(postData['first_name']) < 3:
            errors.append('First name cannot be shorter than 2 characters')
        elif not NAME_REGEX.match(postData['first_name']):
            errors.append('First name is only alphbets!')

        if len(postData['last_name']) < 3:
            errors.append('Last name cannot be shorter than 2 characters')
        elif not NAME_REGEX.match(postData['last_name']):
            errors.append('Last name is only alphbets!')

        if len(postData['password']) < 8:
            errors.append('Password cannot be shorter than 8 characters')
        elif postData['password'] != postData['confirm_password']:
            errors.append('Password is Incorrect and not match')

        user = None
        if len(errors) == 0:
            pw_hash = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pw_hash)

        return {"errors": errors, "user": user}

    def login(self, postData):
        user_list = User.objects.filter(email=postData['email'])
        if not user_list:
            return {"status":False, "user": None}

        pw_hash = user_list[0].password.encode()
        if not bcrypt.checkpw(postData['password'].encode(), pw_hash):
            return {"status":False, "user": None}
        else:
            return {'status': True, "user":user_list[0]}






class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
