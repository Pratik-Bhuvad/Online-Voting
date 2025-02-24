from django.db import models
from users.models import CustomUser
from candidates.models import Candidate

class Vote(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.voter.username} voted for {self.candidate.user.username}'
