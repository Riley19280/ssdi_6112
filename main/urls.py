from django.urls import include, path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('instructions', views.instructions, name='instructions')
]