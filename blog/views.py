from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from itertools import chain
from django.db.models import CharField, Value

from . import forms, models


@login_required
def home(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    reviews = models.Review.objects.filter(user=current_user)

    # Récupération des Abonnés
    users_followed = current_user.followed_by.all()

    users_followed_data = users_followed.values('user')
    users_followed_ids = [data['user'] for data in users_followed_data]

    tickets_users_followed = models.Ticket.objects.filter(
        user__in=users_followed_ids
        )
    reviews_users_followed = models.Review.objects.filter(
        user__in=users_followed_ids
        )
    
    # tickets dont la review a été effectué
    tickets_ids = [review.ticket.id for review in reviews]
    tickets_ids_users_followed = [review.ticket.id for review in reviews_users_followed]
    tickets_ids_reviewed = tickets_ids + tickets_ids_users_followed
    
    tickets = tickets.annotate(content_type=Value('Ticket', CharField()))
    reviews = reviews.annotate(content_type=Value('Review', CharField()))
    tickets_users_followed = tickets_users_followed.annotate(
        content_type=Value('Ticket', CharField())
        )
    reviews_users_followed = reviews_users_followed.annotate(
        content_type=Value('Review', CharField())
        )

    posts = sorted(
        chain(reviews,
              tickets,
              tickets_users_followed,
              reviews_users_followed
              ),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request,
                  "blog/home.html",
                  {"posts": posts, "tickets_ids_reviewed": tickets_ids_reviewed})


@login_required
def AllPostsView(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    reviews = models.Review.objects.filter(user=current_user)
    tickets = tickets.annotate(content_type=Value('Ticket', CharField()))
    reviews = reviews.annotate(content_type=Value('Review', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, "blog/posts.html", context={"posts": posts})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    return render(request, 'blog/create_ticket.html', context={'form': form})


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=ticket)
    return render(request, "blog/update_ticket.html", context={'form': form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect("posts")

    return render(request,
                  "blog/delete_ticket.html",
                  context={"ticket": ticket})


@login_required
def ticket_view(request, post_id):
    ticket = get_object_or_404(models.Ticket, id=post_id)

    return render(request, "blog/ticket.html",
                  context={"ticket": ticket})


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("posts")
    return render(
                    request,
                    "blog/create_review.html",
                    context={
                        "review_form": review_form,
                        "ticket_form": ticket_form
                        }
                    )


@login_required
def create_review(request, ticket_id):
    post = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()

    if request.method == 'POST':

        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = post
            review.save()
            return redirect("posts")
    return render(request, "blog/create_review.html",
                  context={"review_form": review_form, "post": post}
                  )


@login_required
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = review.ticket
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("posts")
    else:
        review_form = forms.ReviewForm(instance=review)
    return render(request, "blog/update_review.html",
                  context={"review_form": review_form, "ticket": ticket})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request,
                  "blog/delete_review.html",
                  context={"review": review})


@login_required
def follow_user(request):
    user = request.user
    follows = models.UserFollows.objects.filter(followed_user=user)
    followers = models.UserFollows.objects.filter(user=user)

    follows_list = [follow.user for follow in follows]
    form = forms.FollowForm(user_exclude=user, follows_list=follows_list)

    if request.method == "POST":
        form = forms.FollowForm(request.POST, user_exclude=user, follows_list=follows_list)

        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.followed_user = user
            subscription.save()
            return redirect('subscriptions')

    return render(request, "blog/subscriptions.html",
                  context={
                    "form": form,
                    "follows": follows,
                    "followers": followers}
                  )


@login_required
def unfollow_user(request, user_follow_id):
    user_follow = get_object_or_404(models.UserFollows, id=user_follow_id)
    if request.method == "POST":
        user_follow.delete()
        return redirect("subscriptions")

    return render(request,
                  "blog/unfollow_user.html",
                  context={"user_follow": user_follow}
                  )
