from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A class represent a user.

    Arguments:
        AbstractUser -- an abstract user class

    Methods:
        unicode -- render an object in a context where
        a string representation is needed.
    """

    def __unicode__(self):
        return self.username
