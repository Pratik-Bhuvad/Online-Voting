from django.db import models
from users.models import CustomUser
from events.models import Event
from django.conf import settings


class Candidate(models.Model):
    POSITION_CHOICES = [
        ('chair_person', 'Chair Person'),
        ('vice_chair_person', 'Vice Chair Person'),
        ('event_head', 'Event Head'),
        ('creativity_head', 'Creative Head'),
        ('hr_head', 'HR Head'),
        ('pr_head', 'PR Head'),
        ('ond_head', 'OND Head'),
        ('finance_head', 'Finance Head'),
        ('digital_head', 'Digital Head'),
            ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profiles'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='candidate_profiles'
    )
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        default='other',
        help_text="Select the position the candidate is contesting for."
    )
    profile_details = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.position.title()} ({self.event.name})"
