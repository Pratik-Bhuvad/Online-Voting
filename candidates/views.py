from django.shortcuts import render, get_object_or_404
from .models import Candidate

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return render(request, 'candidates/candidate_detail.html', {'candidate': candidate})
