from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def user_signup(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}!')
      login(request, user)
      return redirect("index")
  else:
    form = UserCreationForm()
  return render(request, "users/signup.html", {"form": form})


def user_login(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      messages.success(request, f'you are successfully logged in {user.username}!')
      return redirect("index")
    else:
      messages.error(request, 'Invalid username or password.')
  
  else:
    form = AuthenticationForm()
  return render(request, "users/login.html", {"form": form})


def user_logout(request):
  logout(request)
  messages.success(request, 'logged out!')
  return redirect('index')