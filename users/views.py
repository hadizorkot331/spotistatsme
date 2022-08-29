import spotipy
from django.shortcuts import render
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def register(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "users/register.html", {"form": form})

    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(request, username=username, password=password)
            django_login(request, user)

            return HttpResponseRedirect(reverse("stats:index"))

        else:
            return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "GET":
        if request.user:
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse("stats:index"))

        form = LoginForm()
        return render(request, "users/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                django_login(request, user)

                return HttpResponseRedirect(reverse("stats:index"))

        return render(
            request,
            "users/login.html",
            {"form": form, "message": "Invalid Credentials"},
        )


@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse("users:login"))
