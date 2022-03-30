from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def user_profile(request):
    return render(request, "user/profile.html")