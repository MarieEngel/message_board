from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from . import models
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@transaction.atomic
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            user = User.objects.get(username=username)
            profile = models.Profile.objects.create(user=user)
            profile.save()

            messages.success(
                request, f"Account created for {username}!", fail_silently=True
            )
            return redirect(reverse("user:login"))
    else:
        form = UserRegisterForm()
    return render(request, "user/register.html", {"form": form})


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
    return render(request, "user/profile.html")


@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return redirect("home")

    return render(request, "user/delete_user.html", {"user": user})
