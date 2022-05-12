from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

@login_required
def organizerHome(request):
    return render(request, 'events/index.html')

