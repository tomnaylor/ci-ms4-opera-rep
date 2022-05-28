from django.shortcuts import render
from django.db.models import Sum, Count
from donations.models import Donation
from profiles.models import UserLike, UserComment
from works.models import (
                     Production,
                     ProductionVideo,
                     ProductionPhoto)


def index(request):
    """ A view to return index page """

    four_most_liked_id = UserLike.objects.values(
        'production_id').annotate(
            production_count=Count('production_id')).order_by(
                '-production_count')[:4]

    four_most_liked = Production.objects.filter(
        pk__in=[item['production_id'] for item in four_most_liked_id])

    user_comments = UserComment.objects.filter().order_by('-record_added')[:8]

    donation_total = Donation.objects.aggregate(Sum('donation_total'))

    prod_videos = ProductionVideo.objects.order_by('-record_added')[:4]
    prod_photos = ProductionPhoto.objects.order_by('-record_added')[:10]

    productions = Production.objects.all().order_by(
        '-production_premiere',
        'work__name')

    context = {
        'four_most_liked': four_most_liked,
        'user_comments': user_comments,
        'donation_total': donation_total,
        'prod_videos': prod_videos,
        'prod_photos': prod_photos,
        'productions': productions,
    }

    return render(request, 'home/index.html', context)
