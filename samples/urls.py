from django.urls import path

from . import views

urlpatterns = [
    path('', views.SampleListView.as_view(), name='index'),
    path('new/', views.newSampleForm, name='new'),
]
