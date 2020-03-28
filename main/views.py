from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'main/dashboard.html')


def instructions(request):
    return render(request, 'main/instructions.html')


def index(request):
    return render(request, 'main/index.html')