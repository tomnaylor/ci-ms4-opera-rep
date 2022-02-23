from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Work, Production, ProductionMedia, Role, People
from django.db.models import Q
from django.contrib import messages



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

    context = {
        'roles': roles,
        'person': person,
        'productions': productions,
    }

    return render(request, 'works/person.html', context)


def search(request):
    """ Search all works, productions, people and media """

    #productions = Production.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'query' in request.GET:
            query = request.GET['query']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('home'))

            queries = Q(tagline__icontains=query) | Q(synopsis__icontains=query) | Q(year__icontains=query)
            productions = Production.objects.filter(queries)

            queries = Q(name__icontains=query) | Q(synopsis__icontains=query) | Q(tagline__icontains=query)
            people = People.objects.filter(queries)



    current_sorting = f'{sort}_{direction}'

    context = {
        'productions': productions,
        'people': people,
        'query': query,
        'sort': current_sorting,
    }
    print(productions)
    print("kjkjkjkj")
    return render(request, 'works/search.html', context)
