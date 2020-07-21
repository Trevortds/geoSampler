from django.urls import path

from . import views

urlpatterns = [
    path('', views.SampleListView.as_view(), name='index'),
    path('new/', views.newSampleForm, name='new'),
    path('export/csv', views.export, name='download_csv'),
]
