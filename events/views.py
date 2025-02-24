from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Candidate, Vote

@login_required(login_url='login')
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


@login_required(login_url='login')
def vote_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    candidates = Candidate.objects.filter(event=event)
    user_voted = Vote.objects.filter(user=request.user, event=event).exists()

    if request.method == 'POST' and not user_voted:
        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(Candidate, id=candidate_id)
        Vote.objects.create(user=request.user, candidate=candidate, event=event)
        messages.success(request, 'Vote cast successfully!')
        return redirect('dashboard')

    return render(request, 'events/vote_page.html', {'event': event, 'candidates': candidates, 'user_voted': user_voted})
