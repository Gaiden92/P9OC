from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """A class representation of a validator if password
    has at least 1 letter.
    """

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir au minimum 1 lettre.",
                code="password_no_letter",
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au minimum 1 lettre."


class ContainsNumberValidator:
    """A class representation of a validator if password
    has at least 1 number.
    """

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir au minimum 1 chiffre.",
                code="password_no_number",
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au minimum 1 chiffre."
