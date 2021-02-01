# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from verifications.forms import NewVerificationForm


@login_required
def new_verification(request):
    if request.method == 'POST':
        form = NewVerificationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.instance.page_id = request.POST['page']
            form.save()
            return HttpResponseRedirect(reverse("pages:page_verifications",
                                                kwargs={"page_id": request.POST['page']}))
    else:
        form = NewVerificationForm()
    return render(
        request,
        'utils/form.html',
        {
            'title': "Nouvelle vérification",
            'form': form,
        }
    )
