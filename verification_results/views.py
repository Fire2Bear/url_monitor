from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from verification_results.models import VerificationResult


@login_required
def verification_results_by_page(request, page_id):
    verification_results = VerificationResult.objects.filter(
        verification__page=page_id,
    ).order_by(
        "-created",
    )

    return render(
        request,
        "verification_results/verification_results_by_page.html",
        {
            'verification_results': verification_results,
        }
    )
