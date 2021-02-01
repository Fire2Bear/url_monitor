from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from users.forms import AccountSettingsForm, RegisterForm
from users.models import UserProfile


def hello(request):
    return render(
        request,
        'users/hello.html',
        {
            'message': "Hello World!",
        }
    )


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:hello"))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['raw_password']
            user = UserProfile.objects.create_user(
                username=username,
                email=email,
                password=raw_password,
            )
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("users:hello"))
    else:
        form = RegisterForm()
    return render(
        request,
        'utils/form.html',
        {
            'url_form': reverse("users:register"),
            'title': "Inscription",
            'form': form,
        })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:hello"))
    elif 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse("pages:page_list"))
        else:
            return render(
                request,
                'users/login.html',
                {
                    "auth_error": True,
                }
            )
    else:
        return render(
            request,
            'users/login.html',
            {}
        )


@login_required
def myaccount(request):
    return render(
        request,
        'users/myaccount.html',
    )


@login_required
def account_settings(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:

        # print(request.user)
        # print("User : "+str(request.user))
        # print("User : %s" % (str(request.user), ) )

        form = AccountSettingsForm(instance=request.user)
    return render(
        request,
        'utils/form.html',
        {
            'title': "Configuration de compte",
            'form': form,
        }
    )
