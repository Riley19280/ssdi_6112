from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST.copy())

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/dashboard')
        else:
            form.data['password1'] = None
            form.data['password2'] = None
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
