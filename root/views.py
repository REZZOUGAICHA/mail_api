from django.shortcuts import render

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.conf import settings


def index(request):
    return redirect('http://127.0.0.1:8000/')