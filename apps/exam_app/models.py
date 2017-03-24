from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        # Handle all the errors from the registration
        # Check if the name is longer than 2 characters and only contains alphabet characters.
        if not (len(postData['name']) > 2):
            errors.append('Name must be longer than one character')
            if not all((x.isalpha() or x.isspace()) for x in postData['name']):
                errors.append('Name cannot contain any numbers and must be longer than one character')
        # Check if alias is longer than 2 characters and contains only characters
        if not (len(postData['alias']) > 2 and postData['alias'].isalpha()):
            errors.append('Alias cannot contain any numbers and must be longer than one character')
        # Check if the password is greater than or equal to 8 characters
        if len(postData['password']) <= 8:
            errors.append('Password must be at least 8 characters long')
            # Make sure there is at least one capital letter and a number in the password field
            if not PASS_REGEX.match(postData['password']):
                errors.append('Password must contain one number and one uppercase letter')
        # Check if the two password fields are a match
        if postData['password'] != postData['confirm_password']:
            errors.append('Password and confirm password must match')
        # The email field must follow specific syntax
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid Email")
        # Check the birthday
        try:
            dos = datetime.strptime(postData['birthday'], '%m/%d/%Y')
            if datetime.now() < dos:
                errors.append('You are from the future?!')
        except:
            errors.append("Invalid Birthday")
        # Check if the email is already registered
        try:
            User.objects.get(email = postData['email'])
            errors.append('Email is already registered')
        except ObjectDoesNotExist:
            pass
        # If there are no errors, create new User object
        if len(errors) == 0:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name = postData['name'], alias = postData['alias'], password = hashed, email = postData['email'], birthday = postData['birthday'])
            return (True, user)
        return (False, errors)
    def login(self, postData):
        errors = []
        # Try to find the user in the database using the inputted email
        try:
            user = User.objects.get(email = postData['email'])
            password = postData['password']
            #If there is a user, make sure the password is matching
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                return (True, user)
            errors.append("You entered the wrong password.")
        except ObjectDoesNotExist:
            errors.append("The user does not exist")
        return (False, errors)

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    email = models.EmailField()
    birthday = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Try using this
    objects = UserManager()

class PostManager(models.Manager):
    def validatePost(self, postData, userID):
        errors = []
        if len(postData['author']) < 3:
            errors.append('The person who made the quote must have at least three characters')
        if len(postData['content']) < 10:
            errors.append('The quote must be longer than ten characters')
        if len(errors) == 0:
            quote = Quote.objects.create(author = postData['author'], user = userID, content = postData['content'])
            return (True, quote)
        return (False, errors)
    def favorite_quote(self, user_id, quote_id):
        quote = self.get(id = quote_id)
        userFavs = User.objects.get(id = user_id)
        user_Favorites = User.objects.filter(favQuote=quote, id = user_id)
        quote.favorites.add(userFavs)
        return True
    def unfavorite_quote(self, user_id, quote_id):
        quote = self.get(id = quote_id)
        userFavs = User.objects.get(id = user_id)
        user_Favorites = User.objects.filter(favQuote=quote, id = user_id)
        quote.favorites.remove(userFavs)
        return True

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    user = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    favorites = models.ManyToManyField(User, related_name = 'favQuote')
    objects = PostManager()
