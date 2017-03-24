from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
from django.db.models import Count
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'exam_app/index.html')

def process(request):
    # If the button that was pushed is register, it will validate the information
    if request.POST['button'] == 'register':
        register = request.POST
        user = User.objects.register(register)
        # Method returns a tuple and if it is false, it will also return an array containing errors
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        # If there are no errors, it will return True and the user object
        request.session['id'] = user[1].id
        return redirect('/quotes')
    # If the form button pushed was login, it will go through validation for the user
    if request.POST['button'] == 'login':
        user = User.objects.login(request.POST)
        # If the user does not exist or the password does not match the database, errors are returned
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        # If login was successful, the user object is returned
        else:
            request.session['id'] = user[1].id
            return redirect('/quotes')

def success(request):
    if request.session.get('id') == None:
        return redirect('/')
    try:
        userFavorite = []
        otherQuotes = []
        quotes = Quote.objects.all()
        context = {
            'user': User.objects.get(id = request.session['id']),
            'userFavorites': userFavorite,
            'quotes': quotes
        }
    except User.DoesNotExist:
        messages.warning(request, 'User does not exist')
    return render(request, 'exam_app/quotes.html', context)

def add(request):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.validatePost(request.POST, user)
    if quote[0] == False:
        for error in quote[1]:
            messages.warning(request,error)
    return redirect('/quotes')

def favorites(request, id):
    if request.POST['list'] == 'add':
        user = User.objects.get(id = request.session['id'])
        Quote.objects.favorite_quote(request.session['id'], id)
    elif request.POST['list'] == 'remove':
        user = User.objects.get(id = request.session['id'])
        Quote.objects.unfavorite_quote(request.session['id'], id)
    return redirect('/quotes')

def user(request, id):
    context = {
        'user': User.objects.get(id = id),
        'quotes': Quote.objects.filter(user = id),
        'numOfQuotes': Quote.objects.filter(user = id).count()
    }
    return render(request, 'exam_app/users.html', context)

def logout(request):
    request.session.pop('id')
    return redirect('/')
