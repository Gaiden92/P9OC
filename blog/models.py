from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """A class representation of a ticket.

    Arguments:
        models -- a model class

    Methods:
        __str__ -- return the string representation
                    of the class
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    title = models.CharField(
        max_length=128,
    )
    description = models.CharField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    """A class representation of a review

    Arguments:
        models -- a class model

    Methods:
        __str__ -- return the string representation
                    of the class
    """
    ratechoices = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    )
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.headline


class UserFollows(models.Model):
    """A class representation of the suscribe system.

    Arguments:
        models -- a class model
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
