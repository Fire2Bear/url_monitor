# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from pages.forms import NewPageForm
from pages.models import Page


@login_required
def page_list(request):
    pages = Page.objects.filter(
        user=request.user,
    ).order_by(
        "-created",
    )

    return render(
        request,
        "pages/page_list.html",
        {
            'pages': pages,
        }
    )


@login_required
def page_verifications(request, page_id):
    page = Page.objects.prefetch_related('verification_set').get(id=page_id)
    print("page")
    print(page)
    return render(
        request,
        "pages/page_verifications.html",
        {
            'page': page,
        }
    )


@login_required
def new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("pages:page_list"))
    else:
        form = NewPageForm()
    return render(
        request,
        'utils/form.html',
        {
            'title': "Nouvelle page",
            'form': form,
        }
    )
