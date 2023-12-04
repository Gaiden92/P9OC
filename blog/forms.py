from django import forms

from . import models
from authentication import models as a_models
from django.forms.widgets import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    """A class representation of a clearable
    file input

    Arguments:
        ClearableFileInput -- a class clearablefileinput
    """
    initial_text = ""
    input_text = "Télécharger"
    clear_checkbox_label = ""
    template_name = "blog/my_clearable_file_input.html"


class TicketForm(forms.ModelForm):
    """A class representation of a ticket form

    Arguments:
        forms -- a ticket's model form
    """
    image = forms.ImageField(
        label_suffix="", required=False, widget=MyClearableFileInput, label=""
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 10, "cols": 50}),
        }
        labels = {"title": "Titre",
                  "description": "Description",
                  "image": "Hello"}


class ReviewForm(forms.ModelForm):
    """A class representation of a review form.

    Arguments:
        forms -- a review's model form
    """
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(choices=models.Review.ratechoices),
            "body": forms.Textarea(attrs={"rows": 5, "cols": 10}),
        }
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}


class FollowForm(forms.ModelForm):
    """A class representation of a suscribe form

    Arguments:
        forms -- a follow's model form
    """
    class Meta:
        model = models.UserFollows
        fields = ["user"]
        labels = {"user": ""}

    def __init__(self, *args,
                 user_exclude: object = None,
                 follows_list: list = None
                 ) -> None:
        """A class constructor for a follow form.

        Keyword Arguments:
            user_exclude -- the actual user (default: {None})
            follows_list -- the user's follows list (default: {None})
        """
        super(FollowForm, self).__init__(*args)
        self.fields["user"].empty_label = "Nom d'utilisateur"

        if user_exclude:
            self.fields["user"].queryset = (
                a_models.User.objects.all()
                .exclude(is_superuser=True)
                .exclude(username=user_exclude)
                .exclude(username="admin")
            )
            if follows_list:
                self.fields["user"].queryset = (
                    a_models.User.objects.all()
                    .exclude(is_superuser=True)
                    .exclude(username=user_exclude)
                    .exclude(username="admin")
                    .exclude(username__in=follows_list)
                )
