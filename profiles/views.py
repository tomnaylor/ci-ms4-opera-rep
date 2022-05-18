from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from works.models import Production
from .models import UserProfile, UserLike, UserComment
from .forms import UserProfileForm, ProductionCommentForm


@login_required
def profile(request):
    """ Display the user's profile. """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_likes = UserLike.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           ('Update failed. Please ensure '
                            'the form is valid.'))
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'profile': user_profile,
        'likes': user_likes,
        'form': form,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def comment_remove(request, comment_id):
    """ Remove comment """

    user_comment = get_object_or_404(UserComment, pk=comment_id)

    if user_comment.user == request.user:
        try:
            user_comment.delete()
            messages.success(request, 'Comment has been deleted')

        except Exception as e:
            messages.error(request, f'Error deleting comment: {e}')

    else:
        messages.error(request, 'Not correct user')

    return redirect(reverse('production',
                            kwargs={'slug': user_comment.production.url}))


@login_required
def comment_add(request, prod_id):
    """ Add new comment """

    prod = get_object_or_404(Production, pk=prod_id)

    if request.method == 'POST':
        form = ProductionCommentForm(request.POST)

        new_comment = form.save(commit=False)
        new_comment.production = prod
        new_comment.user = request.user

        if form.is_valid():
            new_comment.save()
            messages.success(request, 'comment added successfully')
        else:
            messages.error(request,
                           ('Update failed. Please ensure '
                            'the form is valid.'))

    return redirect(reverse('production', kwargs={'slug': prod.url}))
