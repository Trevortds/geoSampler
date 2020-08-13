from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
# Create your views here.
from django.utils.http import is_safe_url
from guardian.shortcuts import assign_perm

from jobs.forms import JobForm


@login_required
def new_job_form(request):

    form = JobForm(request.POST or None)
    context = {
        "form": form
    }

    next_ = request.GET.get("next")
    print(next_)
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if redirect_path:
        context["next_url"] = redirect_path

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        instance.save()
        if not request.user.has_perm('view_this_job', instance):
            assign_perm('view_this_job', request.user, instance)
            assign_perm('view_job', request.user, instance)
            assign_perm('change_job', request.user, instance)

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("samples:index")

    return render(request, 'jobs/new.html', context)