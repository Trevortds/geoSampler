import csv
import random

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from tablib import Dataset

from geo.utils import random_string_generator
from .admin import SampleResource
from .filters import SampleFilter
from .forms import SampleForm
from .models import Sample
from .tables import SampleTable
# Create your views here.

# def index(request):
#     model = Sample
#     table_class = SampleTable
#     template_name = 'samples/index.html'
#     samples = Sample.objects.all()
#     return render(request, 'samples/index.html', locals())


class SampleListView(FilterView, SingleTableView):
    model = Sample
    table_class = SampleTable
    template_name = 'samples/index.html'

    filterset_class = SampleFilter
    # filter = SampleFilter(queryset=Sample.objects.all())


def newSampleForm(request):
    form = SampleForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        instance.save()

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("samples:index")

    return render(request, 'samples/new.html', context)


def csv_export(request):
    sample_resource = SampleResource()
    dataset = sample_resource.export()  # TODO add a filter here by including queryset as arg to export
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response["Content-Disposition"] = 'attachment; filename="samples.csv'
    return response


def csv_import(request):
    if request.method == 'POST':
        # this should never run, but leaving it here in case i decide to go back to the tablib method
        sample_resource = SampleResource()
        dataset = Dataset()
        new_samples = request.FILES['myfile']

        imported_data = dataset.load(new_samples.read())
        result = sample_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            sample_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'samples/import.html')

def csv_import2(request):
    if request.method == 'POST':
        print(request.POST)
        if 'myfile' in request.FILES:
            # digest file and display field mapping
            print(request.FILES['myfile'])
            filepath = settings.MEDIA_ROOT + "/" + random_string_generator() + request.FILES['myfile'].name
            with open(filepath, 'wb') as f:
                for chunk in request.FILES['myfile'].chunks():
                    f.write(chunk)
            request.session['upload_filepath'] = filepath
            request.session['upload_filename'] = request.FILES['myfile'].name
            print(dict(request.session))

            # get fields in file and fields available in database, try to match them up. Give 4 lists to the template

            render(request, 'samples/import2.html')
        elif 'some_kind_of_form_response' in (data := request.POST.copy()):
            # start import of mapping with data, check for overlapping ids, etc
            pass
        else:
            # return 400
            return HttpResponseBadRequest()
    return render(request, 'samples/import2.html')