from django.shortcuts import render, redirect

# Create your views here.


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'main/dashboard.html')
    else:
        return redirect('login')



def instructions(request):
    return render(request, 'main/instructions.html')


def index(request):
    return render(request, 'main/index.html')