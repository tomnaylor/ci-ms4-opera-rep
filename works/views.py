from django.shortcuts import render
from .models import Work, Production



def all_works(request):
    """ View to display all opera works """

    works = Work.objects.all()

    context = {
        'works': works,
    }

    return render(request, 'works/works.html', context)


def all_productions(request):
    """ View to display all opera productions (tied to a work) """

    productions = Production.objects.all()

    context = {
        'productions': productions,
    }

    return render(request, 'works/productions.html', context)

