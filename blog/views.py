from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from itertools import chain
from django.db.models import CharField, Value

from . import forms, models


@login_required
def home(request: str) -> object:
    """Fonction permettant d'afficher la vue "home"
    et le flux

    Arguments:
        request -- une requête

    Returns:
        un objet HttpResponse avec la liste des postes
        (billets et critiques) ainsi que la liste des id 
        des billets ayant déjà reçus une critique.
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

    tickets = tickets.annotate(content_type=Value("Ticket", CharField()))
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
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
        {"posts": posts, "tickets_ids_reviewed": tickets_ids_reviewed},
    )


@login_required
def AllPostsView(request: str) -> object:
    """Fonction permettant d'afficher la vue "posts"

    Arguments:
        request -- une requête

    Returns:
        un objet HttpResponse contenant la liste des billets
        et des critiques de l'utilisateur.
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
    """Fonction permettant de créer un billet.

    Arguments:
        request -- une requête

    Returns:
        un objet HttpResponse contenant le formulaire
        de sauvegarde d'un billet.
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
    """Fonction permettant de modifier un billet.

    Arguments:
        request -- une requête
        ticket_id -- l'id du billet à modifier

    Returns:
        un objet HttpResponss contenant le formulaire
        de mise à jour du billet.
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
    """Fonction permettant de supprimer un billet.

    Arguments:
        request -- une requête
        ticket_id -- l'idée du ticket à supprimer

    Returns:
        un objet HttpResponse contenant le formulaire
        de suppression d'un billet.
    """
    post = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts")

    return render(request,
                  "blog/delete_ticket.html",
                  context={"post": post})


@login_required
def ticket_view(request: str, post_id: int) -> object:
    ticket = get_object_or_404(models.Ticket, id=post_id)

    return render(request, "blog/ticket.html", context={"ticket": ticket})


@login_required
def create_ticket_and_review(request: str) -> object:
    """Fonction permettant de créer un billet et une critique.

    Arguments:
        request -- une requête

    Returns:
        un objet HttpResponse contenant le formulaire
        de création d'un billet et d'une critique.
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
    """Fonction permettant de créer une critique.

    Arguments:
        request -- une requête
        ticket_id -- l'id d'un billet

    Returns:
        un objet HttpResponse contenant le formulaire
        de création d'une critique.
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
    """Fonction permettant de mettre à jour une critique.

    Arguments:
        request -- une requête
        review_id -- l'id de la critique à modifier

    Returns:
        un objet HttpResponse contenant le formulaire
        de modification d'une critique.
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
    """Fonction permettant de supprimer une critique.

    Arguments:
        request -- une requête
        review_id -- l'id de la critique à supprimer

    Returns:
        un objet HttpResponse contenant le formulaire
        de suppression d'une critique.
    """
    post = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts")

    return render(request,
                  "blog/delete_review.html",
                  context={"post": post})


@login_required
def follow_user(request: str) -> object:
    """Fonction permettant à l'utilisateur 
    de s'abonner à un autre utilisateur.

    Arguments:
        request -- une requête

    Returns:
        un objet HttpResponse contenant le formulaire d'abonnement
        ainsi que la liste des abonnés et des abonnements.
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
    """Fonction permettant de se désabonner d'un utilisateur.

    Arguments:
        request -- une requête
        user_follow_id -- l'id de l'utilisateur à se désabonner

    Returns:
        un objet HttpResponse contenant le formulaire 
        de désabonnement
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
