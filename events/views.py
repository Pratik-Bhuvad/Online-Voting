from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration, Vote
from candidates.models import Candidate


# 📅 Event List View
@login_required
def event_list(request):
    events = Event.objects.all()
    registered_events = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)
    voted_events = Vote.objects.filter(user=request.user).values_list('event_id', flat=True)

    context = {
        'events': events,
        'registered_events': registered_events,
        'voted_events': voted_events,
    }
    return render(request, 'events/event_list.html', context)

from collections import defaultdict

@login_required
# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from events.models import Event, Vote, EventRegistration
# from candidates.models import Candidate

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    candidates = Candidate.objects.filter(event=event).order_by('position')

    # Check if user is registered for the event
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()

    # Get positions for which the user has already voted
    voted_positions = Vote.objects.filter(user=request.user, event=event).values_list('candidate__position', flat=True)

    # Group candidates by position
    position_groups = {}
    for candidate in candidates:
        position_groups.setdefault(candidate.position, []).append(candidate)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'position_groups': position_groups,
        'is_registered': is_registered,
        'voted_positions': voted_positions
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventRegistrationForm


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "✅ You are already registered for this event.")
        return redirect('event_detail', event_id=event_id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user  # Username linked here
            registration.event = event
            registration.save()
            messages.success(request, "🎉 Registration successful!")
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventRegistrationForm()

    return render(request, 'events/register_form.html', {'form': form, 'event': event})



# 🗳️ Voting Function (only if registered and not voted yet)
@login_required
def vote_for_candidate(request, event_id, candidate_id):
    event = get_object_or_404(Event, id=event_id)
    candidate = get_object_or_404(Candidate, id=candidate_id, event=event)

    # ✅ Check if user is registered
    if not EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You need to register for this event before voting.")
        return redirect('events')

    # ✅ Check if user has already voted for the same position
    if Vote.objects.filter(user=request.user, event=event, position=candidate.position).exists():
        messages.error(request, f"You have already voted for the position: {candidate.position}.")
        return redirect('events')

    # ✅ Cast the vote
    Vote.objects.create(user=request.user, candidate=candidate, event=event, position=candidate.position)
    messages.success(request, f"You have successfully voted for {candidate.user.username} as {candidate.position}.")
    return redirect('events')

from django.http import JsonResponse
from django.db.models import Count

@login_required
def event_results(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    candidates = Candidate.objects.filter(event=event).annotate(total_votes=Count('votes')).order_by('-total_votes')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # For AJAX request
        data = []
        for candidate in candidates:
            data.append({
                'name': candidate.user.username,
                'votes': candidate.total_votes,
                'position': candidate.position
            })
        return JsonResponse({'results': data})
    
    winner = candidates.first() if candidates else None
    return render(request, 'events/event_results.html', { 'event': event, 'candidates': candidates, 'winner': winner
    })


    # return render(request, 'events/event_results.html', {'event': event, 'candidates': candidates})