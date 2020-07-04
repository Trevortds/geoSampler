from django.http import HttpResponse
from django.shortcuts import render
from .models import Sample
from django_tables2 import SingleTableView
from .tables import SampleTable
# Create your views here.

# def index(request):
#     model = Sample
#     table_class = SampleTable
#     template_name = 'samples/index.html'
#     samples = Sample.objects.all()
#     return render(request, 'samples/index.html', locals())

class SampleListView(SingleTableView):
    model = Sample
    table_class = SampleTable
    template_name = 'samples/index.html'

def newSampleForm(request):
    return render(request, 'samples/new.html', locals())