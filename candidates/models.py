from django.db import models
from users.models import CustomUser
from events.models import Event
from django.conf import settings

class Candidate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profiles'  # Different related_name for user
    )
    event = models.ForeignKey(
        'events.Event',  # Reference the correct Event model if needed
        on_delete=models.CASCADE,
        related_name='candidate_profiles'  # 👈 Unique related_name for event
    )
    profile_details = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - Profile"
