from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def landing(request):
    return render(request, 'home/landing.html')
