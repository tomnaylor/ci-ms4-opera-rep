from django.shortcuts import render
from works.models import Production

# Create your views here.


def index(request):
    """ A view to return index page """
    
    productions = Production.objects.all()

    context = {
        'productions': productions,
    }

    return render(request, 'home/index.html', context)
