from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'vote_time')
    search_fields = ('voter__username', 'candidate__user__username')
    list_filter = ('vote_time',)
