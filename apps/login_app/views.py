from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages


def index(request):
    return render(request, 'login_app/index.html')

def register(request):
    if request.method == 'POST':
        result = User.objects.register(request.POST)
        if len(result['errors']) == 0:
            request.session['userId'] = result['user'].id
            return redirect('/success')
        for error in result['errors']:
            messages.info(request, error)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        result = User.objects.login(request.POST)
        if result['status']:
            request.session['userId'] = result['user'].id
            return redirect('/success')
        messages.info(request, "Email or password invalid")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if "userId" in request.session:
        user = User.objects.get(id=request.session['userId'])
        context = {"user": user}
        return  render(request, 'login_app/success.html', context)
    return redirect('/')
