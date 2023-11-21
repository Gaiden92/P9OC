from django import forms

from . import models
from authentication import models as a_models

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description" , "image"]
        widgets = { 
                   "description" : forms.Textarea(attrs={'rows':10, 'cols':50})
                   }



class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = [ "headline", "rating", "body"]
        widgets = { "rating" : forms.RadioSelect(choices=models.Review.ratechoices),
                   "body" : forms.Textarea(attrs={'rows':5, 'cols':10})
                   }


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["user"] 



    