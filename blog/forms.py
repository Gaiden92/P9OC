from django import forms

from . import models
from authentication import models as a_models
from django.forms.widgets import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    initial_text = ""
    input_text = "Télécharger"
    clear_checkbox_label = ""
    template_name = "blog/my_clearable_file_input.html"


class TicketForm(forms.ModelForm):
    image = forms.ImageField(
        label_suffix="", required=True, widget=MyClearableFileInput, label=""
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 10, "cols": 50}),
        }
        labels = {"title": "Titre", "description": "Description", "image": "Hello"}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(choices=models.Review.ratechoices),
            "body": forms.Textarea(attrs={"rows": 5, "cols": 10}),
        }
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["user"]
        labels = {"user": ""}

    def __init__(self, *args, user_exclude=None, follows_list=None) -> None:
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
