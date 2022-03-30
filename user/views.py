from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from . import models
from .forms import UserRegisterForm


# Create your views here.
@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            profile = models.Profile.objects.create(user=user)
            profile.save()

            messages.success(request, f'Account created for {username}!', fail_silently=True)  # we can also use add_message() method instead of the shortcuts
            return redirect(reverse('user:login'))
    else:
        form = UserRegisterForm()
    return render(request, "user/register.html", {'form': form})

@login_required
def user_profile(request):
    return render(request, "user/profile.html")