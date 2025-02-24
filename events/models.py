from django.db import models
from users.models import CustomUser
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Candidate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_candidates'  # Unique related_name for user
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='event_candidates'  # 👈 Unique related_name for event
    )
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.name}"



class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='event_votes'  # Updated related_name to avoid conflict
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')  # Ensure one vote per user per event

    def __str__(self):
        return f'{self.user.username} voted for {self.candidate.user.username} in {self.event.name}'
