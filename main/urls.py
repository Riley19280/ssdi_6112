from django.urls import include, path, re_path
from . import views
from django.contrib.staticfiles.views import serve as serve_static



def _static_butler(request, path, **kwargs):
    """
    Serve static files using the django static files configuration
    WITHOUT collectstatic. This is slower, but very useful for API
    only servers where the static files are really just for /admin

    Passing insecure=True allows serve_static to process, and ignores
    the DEBUG=False setting
    """
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    re_path(r'static/(.+)', _static_butler),
    path('', views.index, name='index'),
    path('instructions', views.instructions, name='instructions'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('upload', views.upload, name='upload'),
    path('dataset/<int:dataset_id>', views.delete_dataset, name='delete_dataset'),
    path('data/<str:dataset>/<str:file>', views.serve_graphs, name='serve_graphs')
]

