from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from . import models
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ProfileRegisterForm,
)


@transaction.atomic
def register(request):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get("username")
            user = User.objects.get(username=username)
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(
                request, f"Account created for {username}!", fail_silently=True
            )
            return redirect(reverse("user:login"))
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request, "user/register.html", {"u_form": u_form, "p_form": p_form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == "POST":
        print(request.POST)

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        print(request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            print(request.POST)
            u_form.save()
            p_form.save()
            messages.success(
                request, f"Your account has been updated!", fail_silently=True
            )
            return redirect("user:user-profile")  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "user/update_profile.html", context)


@login_required
def user_profile(request):
    profile = models.Profile.objects.get(user=request.user)
    return render(request, "user/profile.html", {"profile": profile})


@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return redirect("home")

    return render(request, "user/delete_user.html", {"user": user})
