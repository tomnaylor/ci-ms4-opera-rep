""" Views for works """

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Sum
from django.db.models import Q
from django.contrib import messages
from profiles.models import UserLike, UserComment
from profiles.forms import ProductionCommentForm
from donations.models import Donation
from .models import (
                     Work,
                     Production,
                     ProductionVideo,
                     Role,
                     People,
                     ProductionPhoto)


def all_works(request):
    """
    View to display all opera works
    """

    works = Work.objects.all()

    context = {
        'works': works,
    }

    return render(request, 'works/works.html', context)


def all_productions(request):
    """
    View to display all opera productions (tied to a work)
    """

    productions = Production.objects.all()

    context = {
        'productions': productions,
    }

    return render(request, 'works/productions.html', context)


def production(request, slug):
    """
    View to show a production in detail
    """

    # Get this production
    prod = get_object_or_404(Production, url=slug)

    # Search for donations for this production by date and limited to 10
    donations = Donation.objects.filter(
        production=prod.id).order_by('-record_added')[:10]

    # Get sum total of donations towards this production
    donation_total = Donation.objects.filter(
        production=prod.id).aggregate(Sum('donation_total'))

    user_comments = UserComment.objects.filter(production=prod.id)
    prod_videos = ProductionVideo.objects.filter(production=prod.id)
    prod_photos = ProductionPhoto.objects.filter(production=prod.id)
    other_productions = Production.objects.filter(work=prod.work)

    # If the user is logged in
    if request.user.is_authenticated:

        # Search if this request user has liked this production else False
        user_like = UserLike.objects.filter(
            Q(user=request.user) & Q(production=prod)).first()

        # Check if the user has made a comment review before
        previous_comment = UserComment.objects.filter(
            production=prod.id, user=request.user)

        comment_form = ProductionCommentForm(instance=request.user)

        # check if the user has clicked on "like"
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

            return redirect(reverse('production', kwargs={'slug': prod.url}))

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
        'donations': donations,
        'donation_total': donation_total,
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
    """
    View to show a single persons detail
    """

    person = get_object_or_404(People, url=slug)
    roles = Role.objects.filter(person=person.id)

    # get a list of all productions that the person
    # is either in the creative, cast or staff m2m
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
    """
    Search all works, productions, people and media
    """

    productions = Production.objects.all()
    people = People.objects.all()

    query = None
    sort = None
    direction = None

    if request.GET:

        if 'query' in request.GET:
            query = request.GET['query']

            # if no search term used, redirect
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('home'))

            # search thru the production table
            queries = (
                       Q(tagline__icontains=query) |
                       Q(synopsis__icontains=query) |
                       Q(year__icontains=query) |
                       Q(work__name__icontains=query))

            productions = productions.filter(queries)

            # search thru the people table
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
