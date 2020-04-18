from django.shortcuts import render, redirect
from . import forms
from django.conf import settings
import os
import errno
import uuid
from . import models
# Create your views here.


def dashboard(request):
    if request.user.is_authenticated:
        datasets = models.facebook_data_upload.objects.filter(user=request.user)
        return render(request, 'main/dashboard.html', { 'datasets': datasets })
    else:
        return redirect('login')


def instructions(request):
    return render(request, 'main/instructions.html')


def upload(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = forms.DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            saved_file_name = save_file(request.FILES['file'])

            m = models.facebook_data_upload()
            m.dataset_name = form.cleaned_data['dataset_name']
            m.file_name = saved_file_name
            m.upload_file_name = request.FILES['file'].name
            m.user = request.user
            m.save()

            return render(request, 'main/upload-dataset.html', {'form': form, 'isSuccess': True})
        else:
            return render(request, 'main/upload-dataset.html', {'form': form})
    else:
        form = forms.DatasetUploadForm()
    return render(request, 'main/upload-dataset.html', {'form': form})


def index(request):
    return render(request, 'main/index.html')


def save_file(f):
    filename = str(uuid.uuid1()) + '.json'
    base = os.path.join('dataset_uploads', filename)
    filepath = os.path.join(settings.MEDIA_ROOT, base)
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filename
