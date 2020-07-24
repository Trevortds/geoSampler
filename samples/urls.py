from django.urls import path

from . import views

urlpatterns = [
    path('', views.SampleListView.as_view(), name='index'),
    path('new/', views.newSampleForm, name='new'),
    path('export/csv', views.csv_export, name='download_csv'),
    path('import/csv', views.csv_import, name='upload_csv'),
    path('import/csv/2', views.csv_import2, name='upload_csv2'),
]
