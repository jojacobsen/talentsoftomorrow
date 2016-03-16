from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic

@login_required
def home(request):
    return HttpResponse('Home Page')
