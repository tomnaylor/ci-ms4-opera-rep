from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Work, Production, ProductionVideo, Role, People, ProductionPhoto
from profiles.models import UserLike, UserComment
from django.db.models import Q
from django.contrib import messages
from profiles.forms import ProductionCommentForm



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

    user_like = UserLike.objects.filter(Q(user=request.user) & Q(production=prod)).first() if request.user.is_authenticated else False

    user_comments = UserComment.objects.filter(production=prod.id)
    prod_videos = ProductionVideo.objects.filter(production=prod.id)
    prod_photos = ProductionPhoto.objects.filter(production=prod.id)
    other_productions = Production.objects.filter(work=prod.work)

    if request.user.is_authenticated:

        user_like = UserLike.objects.filter(Q(user=request.user) & Q(production=prod)).first()

        previous_comment = UserComment.objects.filter(production=prod.id,user=request.user)

        comment_form = ProductionCommentForm(instance=request.user)

        if 'like' in request.GET:
            if user_like:
                # DELETE LIKE
                user_like.delete()
                messages.success(request, 'Production has been unliked!')
            else:
                # ADD LIKE
                new_like = UserLike(user=request.user, production=prod)
                new_like.save()
                messages.success(request, 'Production liked')

            return redirect(reverse('production', kwargs={ 'slug':prod.url }))

    else:
        user_like = False
        comment_form = False
        previous_comment = False


    creatives = prod.creatives.all()
    cast = prod.cast.all()
    staff = prod.staff.all()


        
    context = {
        'production': prod,
        'user_like': user_like,
        'comments': user_comments,
        'videos': prod_videos,
        'photos': prod_photos,
        'other_productions': other_productions,
        'creatives': creatives,
        'cast': cast,
        'staff': staff,
        'comment_form': comment_form,
        'previous_comment': previous_comment,
        
    }

    return render(request, 'works/production.html', context)


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

    productions = Production.objects.all()
    people = People.objects.all()
    
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'query' in request.GET:
            query = request.GET['query']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('home'))

            queries = Q(tagline__icontains=query) | Q(synopsis__icontains=query) | Q(year__icontains=query) | Q(work__name__icontains=query)
            productions = productions.filter(queries)

            queries = Q(name__icontains=query) | Q(synopsis__icontains=query)
            people = people.filter(queries)



    current_sorting = f'{sort}_{direction}'

    context = {
        'productions': productions,
        'people': people,
        'query': query,
        'sort': current_sorting,
    }
    
    return render(request, 'works/search.html', context)
