from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, "blog/home.html", {"tickets":tickets})


@login_required
def create_ticket(request):
    form = forms.CreateTicketForm()
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        
            return redirect('home')
    return render(request, 'blog/create_ticket.html', context={'form': form})

# @login_required
# def update_ticket(request):
#     form = forms.UpdateTicketForm()
#     if request.method == "POST":
#         form = forms.UpdateTicketForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
        
#     return render(request, "blog/post_view.html", context={'form': form})

@login_required
def AllPostsView(request):
    user = request.user
    tickets = models.Ticket.objects.filter(user=user)
    return render(request, "blog/posts.html", context={"tickets": tickets})

@login_required
def PostView(request, post_id):
    ticket = get_object_or_404(models.Ticket, id=post_id)
    return render(request, "blog/post.html", context={"ticket": ticket})