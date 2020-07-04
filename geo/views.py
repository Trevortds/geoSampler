from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
# from .forms import ContactForm


def home_page(request):
    context = {
        "title": "Our Geology Sample Website!",
        "content": "welcome to the homepage!",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "Woohoo, you're a very special user!"
    return render(request, "index.html", context)