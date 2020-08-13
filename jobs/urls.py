from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.new_job_form, name='new'),
]
