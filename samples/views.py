from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django_filters.views import FilterView
from django_tables2 import SingleTableView

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

def export(request):
    sample_resource = SampleResource()
    dataset = sample_resource.export()  # TODO add a filter here by including queryset as arg to export
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response["Content-Disposition"] = 'attachment; filename="samples.csv'
    return response
