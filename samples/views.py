from django.http import HttpResponse
from django.shortcuts import render
from .models import Sample
# Create your views here.

def index(request):
    istekler = Sample.objects.all()
    return render(request, 'samples/index.html', locals())
