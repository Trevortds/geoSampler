from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
# from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, GuestForm, PasswordChangeForm
from django.utils.http import is_safe_url


# Create your views here.

def logout_page(request):
    logout(request)
    return redirect("/")

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("user logged in?")
    print(request.user.is_authenticated)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        print(request.user.is_authenticated)
        print(user)
        if user is not None:
            login(request, user)
            try:
                del request.session["guest_email_id"]
            except:
                pass
            # context["form"] = LoginForm()
            # redirect to a success page
            if redirect_path and is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # invalid login error message
            print("Failed login")

    return render(request, "accounts/login.html", context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("/")
    return render(request, "accounts/register.html", context)


@login_required
def password_change_page(request):
    form = PasswordChangeForm(request.POST or None, username=request.user.username)
    context = {
        "form": form
    }

    if form.is_valid():
        old_password = form.cleaned_data.get("old_password")
        user = authenticate(username=request.user.username, password=old_password)  # this is duplicate, but w/e
        if user is not None:
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return render(request, "accounts/success.html",
                          {"message": "Password successfully updated, redirecting you to home page"})

    return render(request, "accounts/change_password.html", context)
