from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from itertools import chain
from django.db.models import CharField, Value

from . import forms, models


@login_required
def home(request: str) -> object:
    """Function to display the "home" view
    and the flow

    Arguments:
        request -- a request

    Returns:
        an HttpResponse object with the list of positions
        (tickets and reviews) as well as the list of id
        posts that have already received a review.
    """
    # Récupération de l'utilisateur, de ses billets
    # et de ses critiques
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    reviews = models.Review.objects.filter(user=current_user)

    # Récupération des Abonnés, de leurs billets
    # et de leurs critiques
    users_followed = current_user.followed_by.all()

    users_followed_data = users_followed.values("user")
    users_followed_ids = [data["user"] for data in users_followed_data]

    tickets_users_followed = models.Ticket.objects.filter(
        user__in=users_followed_ids
        )
    reviews_users_followed = models.Review.objects.filter(
        user__in=users_followed_ids
        )

    # tickets dont la review a été effectué
    tickets_ids = [review.ticket.id for review in reviews]
    tickets_ids_users_followed = [
        review.ticket.id for review in reviews_users_followed
        ]
    tickets_ids_reviewed = tickets_ids + tickets_ids_users_followed

    tickets = tickets.annotate(
        content_type=Value("Ticket", CharField())
        )
    reviews = reviews.annotate(
        content_type=Value("Review", CharField())
        )
    tickets_users_followed = tickets_users_followed.annotate(
        content_type=Value("Ticket", CharField())
    )
    reviews_users_followed = reviews_users_followed.annotate(
        content_type=Value("Review", CharField())
    )

    posts = sorted(
        chain(reviews,
              tickets,
              tickets_users_followed,
              reviews_users_followed),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(
        request,
        "blog/home.html",
        {"posts": posts,
         "tickets_ids_reviewed": tickets_ids_reviewed},
    )


@login_required
def AllPostsView(request: str) -> object:
    """Function to display the "posts" view

    Arguments:
        request -- a request

    Returns:
        an HttpResponse object containing the list of tickets
        and user reviews.
    """
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    reviews = models.Review.objects.filter(user=current_user)
    tickets = tickets.annotate(content_type=Value("Ticket", CharField()))
    reviews = reviews.annotate(content_type=Value("Review", CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, "blog/posts.html", context={"posts": posts})


@login_required
def create_ticket(request: str) -> object:
    """Function to create a ticket.

    Arguments:
        request -- a request

    Returns:
        an HttpResponse object containing the form
        saving a ticket.
    """
    form = forms.TicketForm(label_suffix="")
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, label_suffix="")
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")

    return render(request, "blog/create_ticket.html", context={"form": form})


@login_required
def update_ticket(request: str, ticket_id: int) -> object:
    """Function allowing you to modify a ticket.

    Arguments:
        request -- a request
        ticket_id -- the id of the ticket to modify

    Returns:
        an HttpResponss object containing the form
        to update the ticket.
    """
    post = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        form = forms.TicketForm(
            request.POST, request.FILES, instance=post, label_suffix=""
        )

        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=post, label_suffix="")
    return render(request, "blog/update_ticket.html", context={"form": form})


@login_required
def delete_ticket(request: str, ticket_id: int) -> object:
    """Function to delete a ticket.

    Arguments:
        request -- a request
        ticket_id -- the idea of ​​the ticket to delete

    Returns:
        an HttpResponse object containing the form
        deleting a ticket.
    """
    post = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts")

    return render(request, "blog/delete_ticket.html", context={"post": post})


@login_required
def ticket_view(request: str, post_id: int) -> object:
    ticket = get_object_or_404(models.Ticket, id=post_id)

    return render(request, "blog/ticket.html", context={"ticket": ticket})


@login_required
def create_ticket_and_review(request: str) -> object:
    """Function to create a post and a review.

    Arguments:
        request -- a request

    Returns:
        an HttpResponse object containing the form
        creating a post and a review.
    """
    ticket_form = forms.TicketForm(label_suffix="")
    review_form = forms.ReviewForm(label_suffix="")

    if request.method == "POST":
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
        context={"review_form": review_form, "ticket_form": ticket_form},
    )


@login_required
def create_review(request: str, ticket_id: int) -> object:
    """Function to create a review.

    Arguments:
        request -- a request
        ticket_id -- the id of a ticket

    Returns:
        an HttpResponse object containing the form
        creating a review.
    """
    post = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = post
            review.save()
            return redirect("posts")
    return render(
        request,
        "blog/create_review.html",
        context={"review_form": review_form, "post": post},
    )


@login_required
def update_review(request: str, review_id: int) -> object:
    """Function to update a review.

    Arguments:
        request -- a request
        review_id -- the id of the review to modify

    Returns:
        an HttpResponse object containing the form
        modifying a review.
    """
    review = get_object_or_404(models.Review, id=review_id)
    post = review.ticket
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("posts")
    else:
        review_form = forms.ReviewForm(instance=review)
    return render(
        request,
        "blog/update_review.html",
        context={"review_form": review_form, "post": post},
    )


@login_required
def delete_review(request: str, review_id: int) -> object:
    """Function to delete a review.

    Arguments:
        request -- a request
        review_id -- the id of the review to delete

    Returns:
        an HttpResponse object containing the form
        deleting a review.
    """
    post = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts")

    return render(request, "blog/delete_review.html", context={"post": post})


@login_required
def follow_user(request: str) -> object:
    """Function allowing the user
    to subscribe to another user.

    Arguments:
        request -- a request

    Returns:
        an HttpResponse object containing the subscription form
        as well as the list of subscribers and subscriptions.
    """
    user = request.user
    follows = models.UserFollows.objects.filter(followed_user=user)
    followers = models.UserFollows.objects.filter(user=user)

    # Récupération de la liste des utilisateur déjà suivis
    follows_list = [follow.user for follow in follows]
    # Exclusion de l'utilisateur connecté ainsi que
    # des utilisateurs déjà suivis
    form = forms.FollowForm(user_exclude=user, follows_list=follows_list)

    if request.method == "POST":
        form = forms.FollowForm(
            request.POST, user_exclude=user, follows_list=follows_list
        )

        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.followed_user = user
            subscription.save()
            return redirect("subscriptions")

    return render(
        request,
        "blog/subscriptions.html",
        context={"form": form, "follows": follows, "followers": followers},
    )


@login_required
def unfollow_user(request: str, user_follow_id: int) -> object:
    """Function to unsubscribe from a user.

    Arguments:
        request -- a request
        user_follow_id -- the id of the user to unfollow

    Returns:
        an HttpResponse object containing the form
        unsubscribe
    """
    user_follow = get_object_or_404(models.UserFollows, id=user_follow_id)
    if request.method == "POST":
        user_follow.delete()
        return redirect("subscriptions")

    return render(
        request,
        "blog/unfollow_user.html",
        context={"user_follow": user_follow}
    )
