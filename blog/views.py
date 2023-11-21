from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from authentication import models as a_models

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, "blog/home.html", {"tickets":tickets})

@login_required
def AllPostsView(request):
    user = request.user
    tickets = models.Ticket.objects.filter(user=user)
    reviews = models.Review.objects.filter(user=user)

    return render(request, "blog/posts.html", context={"tickets": tickets, "reviews": reviews})

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
    
    return render(request, "blog/delete_ticket.html", context={"ticket": ticket})


@login_required
def create_review(request, ticket_id="None"):
    if ticket_id == "None":
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket_form = forms.TicketForm(instance=ticket)
    else:
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
    return render(request, "blog/create_review.html",
                  context={"review_form":review_form, "ticket_form":ticket_form}
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
                  context={"review_form":review_form,"ticket": ticket}
                )

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request, "blog/delete_review.html", context={ review:review })

@login_required
def follow_user(request):
    user = request.user
    follows = models.UserFollows.objects.filter(followed_user=user)
    followers = models.UserFollows.objects.filter(user=user)
    form = forms.FollowForm()
    already_suscribed = [follow.user for follow in follows]
    form.fields['user'].queryset = a_models.User.objects.all()\
        .exclude(is_superuser=True).exclude(username=user).exclude(
            username__in=already_suscribed
            )
    
    if request.method == "POST":
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.followed_user = user
            subscription.save()
            return redirect('subscriptions')
    return render(request, "blog/subscriptions.html",
                  context={"form":form, "follows":follows, "followers":followers}
                  )

@login_required
def unfollow_user(request, user_follow_id):
    user_follow = get_object_or_404(models.UserFollows, id=user_follow_id)
    if request.method == "POST":
        user_follow.delete()
        return redirect("subscriptions")

    return render(request, "blog/unfollow_user.html", context={"user_follow":user_follow})