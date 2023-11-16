from django import forms

from . import models

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description" , "image"]

class UpdateTicketForm(forms.ModelForm):
    pass 