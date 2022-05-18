from django.shortcuts import render
from works.models import Production

# Create your views here.


def index(request):
    """ A view to return index page """
    
    productions = Production.objects.all().order_by('-production_premiere', 'work__name')

    context = {
        'productions': productions,
    }

    return render(request, 'home/index.html', context)
