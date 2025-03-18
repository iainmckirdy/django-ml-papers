from django.shortcuts import render

from .models import Week, Paper

# Create your views here.

# using .objects.last to get the most recent one for the home page
def home(request):
    return render(request, 'home.html', 
                   {'papers': Week.objects.last().papers.all(), 
                    'weeks': Week.objects.all().order_by('-id'), # order_by('-id') is used so that weeks are shown in decending order in side bar
                    'week': Week.objects.last()})


def post(request, date):
    return render(request, 'post.html', 
                   {'papers': Week.objects.get(date=date).papers.all(), 
                    'weeks': Week.objects.all().order_by('-id'), # order_by('-id') is used so that weeks are shown in decending order in side bar
                    'week': Week.objects.get(date=date)})


def about(request):
    return render(request, 'about.html',
                  {'weeks': Week.objects.all().order_by('-id')})