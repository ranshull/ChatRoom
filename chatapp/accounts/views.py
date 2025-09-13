# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import LoginForm

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # redirect to home after login
#             else:
#                 return render(request, 'login.html', {'form': form, 'error': 'Invalid Credentials'})
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("welcome")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("welcome")
            else:
                return render(request, "login.html", {"form": form, "error": "Invalid credentials"})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def welcome_view(request):
    return render(request, "welcome.html")
