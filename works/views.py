from django.shortcuts import render, get_object_or_404
from .models import Work, Production, ProductionMedia, Role, People
from django.db.models import Q



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


def production(request, slug):
    """ View to show a single production detail """

    prod = get_object_or_404(Production, url=slug)
    prod_media = ProductionMedia.objects.filter(production=prod.id)
    other_productions = Production.objects.filter(work=prod.work)

    creatives = prod.creatives.all()
    cast = prod.cast.all()
    staff = prod.staff.all()

    context = {
        'production': prod,
        'media': prod_media,
        'other_productions': other_productions,
        'creatives': creatives,
        'cast': cast,
        'staff': staff,
    }

    return render(request, 'works/production.html', context)


def production_media(request, media_id):
    """ View to show a media item for a production """

    media_item = get_object_or_404(ProductionMedia, pk=media_id)

    context = {
        'media_item': media_item,
    }

    return render(request, 'works/media.html', context)


def person(request, slug):
    """ View to show a single persons detail """

    person = get_object_or_404(People, url=slug)
    roles = Role.objects.filter(person=person.id)
    productions = Production.objects.filter(
                  Q(creatives__in=roles) |
                  Q(cast__in=roles) |
                  Q(staff__in=roles)).distinct()

    productions = Production.objects.all()

    context = {
        'roles': roles,
        'person': person,
        'productions': productions,
    }

    return render(request, 'works/person.html', context)
