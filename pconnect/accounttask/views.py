from django.shortcuts import render
from accounttask.models import *

# Create your views here.
def home(request):
    posts = Country.objects.all()

    return render(request, 'task/home.html', {
        'posts': posts
    })