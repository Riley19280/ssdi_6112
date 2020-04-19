from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import forms
from django.conf import settings
import os
import errno
import shutil
import uuid
from . import models
from main.graphs import generate_graphs
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

            generate_graphs(request.user, m.dataset_name, os.path.join(settings.MEDIA_ROOT, 'dataset_uploads', m.file_name))

            return render(request, 'main/upload-dataset.html', {'form': form, 'isSuccess': True})
        else:
            return render(request, 'main/upload-dataset.html', {'form': form})
    else:
        form = forms.DatasetUploadForm()
    return render(request, 'main/upload-dataset.html', {'form': form})


def index(request):
    return render(request, 'main/index.html')


def serve_graphs(request, dataset, file):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    dataset_dir = os.path.join(settings.MEDIA_ROOT, 'graphs', str(request.user.id), dataset)
    if not os.path.exists(dataset_dir):
        return HttpResponse('Dataset not found', status=404)

    file_path = os.path.join(dataset_dir, file)
    if not os.path.exists(file_path):
        return HttpResponse('File not found', status=404)

    with open(file_path) as file:
        return HttpResponse(file, content_type="image/svg+xml")


@csrf_exempt
def delete_dataset(request, dataset_id):
    if request.method != 'DELETE':
        return HttpResponse('Method Not Allowed', status=405)

    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    dataset = models.facebook_data_upload.objects.filter(user=request.user, id=dataset_id).first()

    if dataset is None:
        return HttpResponse('Dataset not found', status=404)

    try:
        original_umask = os.umask(0)
        os.remove(os.path.join(settings.MEDIA_ROOT, 'dataset_uploads', dataset.file_name))
    except FileNotFoundError:
        pass
    finally:
        os.umask(original_umask)

    try:
        original_umask = os.umask(0)
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'graphs', str(request.user.id), dataset.dataset_name))
        dataset.delete()
    except FileNotFoundError:
        pass
    except PermissionError as e:
        print(e)
        return HttpResponse('Internal Server Error', status=500)
    finally:
        os.umask(original_umask)

    return HttpResponse('Dataset deleted', status=200)


def save_file(f):
    filename = str(uuid.uuid1()) + '.json'
    base = os.path.join('dataset_uploads', filename)
    filepath = os.path.join(settings.MEDIA_ROOT, base)
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            original_umask = os.umask(0)
            os.makedirs(os.path.dirname(filepath), mode=0o777)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        finally:
            os.umask(original_umask)
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filename

