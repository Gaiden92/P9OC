from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from . import forms


def logout_view(request: str) -> object:
    """Function allowing a user to
    connect.

    Arguments:
        request -- str: a request

    Returns:
        object: an HttpResponse object containing the form
        disconnection.
    """
    logout(request)
    return redirect("login")


def login_view(request: str) -> object:
    """Function allowing a user to log in.

    Arguments:
        request -- str: a request

    Returns:
        object: an HttpResponse object containing the form
        connection.
    """
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides."
    return render(
        request,
        "authentication/login.html",
        context={"form": form, "message": message}
    )


def signup_view(request: str) -> object:
    """Function allowing a user to register.

    Arguments:
        request -- str: a request

    Returns:
        object: an HttpResponse object containing the form
        registration.
    """
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request,
                  "authentication/signup.html",
                  context={"form": form})
