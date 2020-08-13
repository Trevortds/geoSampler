import csv
import random

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
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
from .utils import matchup_fieldnames, mapping_sanity_check, start_processing


class SampleListView(FilterView, SingleTableView):
    model = Sample
    table_class = SampleTable
    template_name = 'samples/index.html'

    filterset_class = SampleFilter
    # filter = SampleFilter(queryset=Sample.objects.all())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['book_list'] = Book.objects.all()
        print(context)
        context['object_list'] = [s for s in context['object_list']
                                  if s in Sample.objects.get_samples_for_user(self.request.user)]
        context['sample_list'] = context['object_list']
        context['table'] = SampleTable(context['sample_list'])
        self.request.session["filter_request"] = context['filter'].request.GET
        print(context)
        print(self.request.user)
        print(self.request.user.username)
        return context

def sample_list_view(request):
    pass


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
    print(request.session.get('filter_request'))
    f = SampleFilter(request.session.get('filter_request'), queryset=Sample.objects.get_samples_for_user(request.user))
    sample_resource = SampleResource()
    dataset = sample_resource.export(queryset=f.qs)
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
    context = {}
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
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                # TODO catch errors here
                input_list = reader.fieldnames


            # form = SampleForm()
            resource = SampleResource()
            # form_field_classes = tuple((field_name, form.fields[field_name].widget.__class__) for field_name in form.fields)
            # model_forms = [pair[0] for pair in form_field_classes]
            model_forms = list(resource.fields.keys())
            input_match, output_match = matchup_fieldnames(input_list, model_forms)
            for x in input_match:
                input_list.remove(x)
            for x in output_match:
                model_forms.remove(x)
            context["input_list"] = input_list
            context["input_match"] = input_match
            context["output_match"] = output_match
            context["model_list"] = model_forms
            context["upload_filename"] = request.session['upload_filename']
            return render(request, 'samples/import2.html', context)
        elif 'select2' in (data := request.POST.copy()) and 'select3' in (data := request.POST.copy()):
            print(data.getlist("select2"))
            valid, error_msg = mapping_sanity_check(data.getlist("select2"),
                                                    data.getlist("select3"),
                                                    request.session['upload_filepath'])
            if valid:
                # TODO Send user to a new view, where they can confirm using the first row as an example
                #   That view may need to have a loading spinner
                request.session["input_match"] = data.getlist("select2")
                request.session["output_match"] = data.getlist("select3")
                request.session["io_message"] = error_msg
                return redirect(reverse("samples:confirm_upload"))

            else:
                with open(request.session['upload_filepath'], 'r') as f:
                    reader = csv.DictReader(f)
                    input_list = reader.fieldnames
                model_forms = list(SampleResource().fields.keys())

                for x in data.getlist("select2"):
                    input_list.remove(x)
                for x in data.getlist("select3"):
                    model_forms.remove(x)
                context["errors"] = error_msg
                context["input_list"] = input_list
                context["input_match"] = data.getlist("select2")
                context["output_match"] = data.getlist("select3")
                context["model_list"] = model_forms
                context["upload_filename"] = request.session['upload_filename']

                return render(request, 'samples/import2.html', context)

            # start import of mapping with data, check for overlapping ids, etc
            # check validity with common sense first, if validity fails send back errors and display in an if block,
            # like this https://stackoverflow.com/questions/14647723/django-forms-if-not-valid-show-form-with-error-message

            return HttpResponseBadRequest("This isn't implemented yet")
        else:
            # return 400
            return HttpResponseBadRequest("Error: Bad request. If you are seeing this page, your form data did not "
                                          "send properly. Please contact webmaster")
    return render(request, 'samples/import2.html', context)

def confirm_upload(request):
    if request.method == 'GET':

        context = {
            "filename" : request.session['upload_filename'],
            "input_match" : request.session["input_match"],
            "output_match": request.session["output_match"],
            "match_pairs": zip(request.session["input_match"], request.session["output_match"]),
            "io_message": request.session["io_message"],
        }
        return render(request, 'samples/import_confirmation.html', context)

    if request.method == 'POST':
        start_processing(request.session["input_match"],
                         request.session["output_match"],
                         request.session['upload_filepath'])
        request.session.flush()

        return redirect('samples:index')