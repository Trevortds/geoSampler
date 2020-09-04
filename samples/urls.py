from django.urls import path

from . import views

urlpatterns = [
    path('', views.SampleListView.as_view(), name='index'),
    # path('<slug:pk>', views.SampleDetailView.as_view(), name='detail'),
    path('<slug:sample_no>', views.SampleDetailSlugView.as_view(), name='detail'),
    path('new/', views.newSampleForm, name='new'),
    path('export/csv', views.csv_export, name='download_csv'),
    path('import/csv', views.csv_import, name='upload_csv'),
    path('import/csv/2', views.csv_import2, name='upload_csv2'),
    path('import/csv/confirm', views.confirm_upload, name='confirm_upload'),
    path('error/', views.throw_an_error),
]
