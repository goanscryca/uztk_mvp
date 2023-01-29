from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ManyToManyField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from uztk.app.models import Camera


class User(AbstractUser):
    """
    Default custom user model for uztk.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    
    GUARD = 1
    roles = [
        (GUARD, 'Охранник')
    ]
    
    role = IntegerField(choices=roles, null=True, blank=True, verbose_name="Роль")
    cameras = ManyToManyField(to=Camera)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
