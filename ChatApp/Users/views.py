from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return redirect("account_signup")


def logout_view(request):
    logout(request)
    return redirect("/")

# @login_required
# def welcome_view(request):
#     return render(request, 'welcome.html', {'username': request.user.username})