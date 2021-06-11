from django.db import models
from datetime import datetime

import re, bcrypt

class LoginManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First Name should be at least 3 characters"
        if len(postData['last_name']) < 5:
            errors["last_name"] = "Last Name should be at least 5 characters" 
        if len(postData['first_name']) < 3:
            errors["username"] = "Username should be at least 3 characters" 
        if len(postData['password']) < 4:
            errors["password"] = "Password should be at least 4 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Password doesn't match"   
        return errors

    def authenticate(self, postData):
        errors = {}
        check = User.objects.filter(username=postData['username'])
        if not check:
            errors['username'] = "Username has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check[0].password.encode()):
                errors['password'] = " Password do not match."
        return errors
        

class BoxManager(models.Manager):
    def box_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors["name"] = "Box name is missing"
        if len(postData['description']) < 2:
            errors["description"] = "Description is missing"     
        if len(postData['qty']) < 1:
            errors["qty"] = "Please put the quantity" 
    
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    objects = LoginManager() 

    def __repr__(self):
        return f"<User object: {self.first_name} ({self.id})>"

class Box(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, related_name='boxes',on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)
    location = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = BoxManager()

    def __repr__(self):
        return f"<Box object: {self.name} ({self.id})>"

   




