from django.db import models
from users.models import CustomUser
from django.conf import settings
from django.apps import apps

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

# class Candidate(models.Model):
#     POSITION_CHOICES = [
#         ('chair_person', 'Chair Person'),
#         ('vice_chair_person', 'Vice Chair Person'),
#         ('event_head', 'Event Head'),
#         ('creativity_head', 'Creative Head'),
#         ('hr_head', 'HR Head'),
#         ('pr_head', 'PR Head'),
#         ('ond_head', 'OND Head'),
#         ('finance_head', 'Finance Head'),
#     ]

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='event_candidate_profiles'
#     )
#     event = models.ForeignKey(
#         'events.Event',
#         on_delete=models.CASCADE,
#         related_name='event_candidate_profiles'
#     )
#     position = models.CharField(
#         max_length=50,
#         choices=POSITION_CHOICES,
#         default='other',
        # help_text="Select the position the candidate is contesting for."
    # )
    # profile_details = models.TextField()

    # def __str__(self):
        # return f"{self.user.username} - {self.position.title()} ({self.event.name})"

class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='event_votes'  # Updated related_name to avoid conflict
    )
    candidate = models.ForeignKey('candidates.Candidate', on_delete=models.CASCADE, related_name='votes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    position = models.CharField(max_length=50) 

    class Meta:
        unique_together = ('user', 'position','event')  # Ensure one vote per user per event

    def __str__(self):
        Candidate = apps.get_model('candidates', 'Candidate')
        candidate = Candidate.objects.get(pk=self.candidate_id)
        return f'{self.user.username} voted for {self.candidate.user.username} in {self.event.name}'


class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    college_id = models.CharField(max_length=50)
    student_class = models.CharField(max_length=100)
    division = models.CharField(max_length=10)
    year = models.CharField(max_length=50)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} ({self.college_id}) registered for {self.event.name}"