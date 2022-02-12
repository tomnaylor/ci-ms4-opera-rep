from django.shortcuts import render, get_object_or_404
from .models import Work, Production, ProductionMedia



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


def production(request, slug, production_id):
    """ View to show a single production detail """

    prod = get_object_or_404(Production, pk=production_id)
    prod_media = ProductionMedia.objects.filter(production=production_id)

    context = {
        'production': prod,
        'media': prod_media,
    }

    return render(request, 'works/production.html', context)


def production_media(request, media_id):
    """ View to show a media item for a production """

    media_item = get_object_or_404(ProductionMedia, pk=media_id)

    context = {
        'media_item': media_item,
    }

    return render(request, 'works/media.html', context)
