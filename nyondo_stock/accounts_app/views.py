from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib import messages  # type: ignore

# Create your views here.


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name='ADMIN').exists():
                return HttpResponse("ADMIN LOGIN SUCCESS")

            elif user.groups.filter(name='MANAGER').exists():
                return HttpResponse("MANAGER LOGIN SUCCESS")

            elif user.groups.filter(name='ATTENDANT').exists():
                return HttpResponse("ATTENDANT LOGIN SUCCESS")

            else:
                return HttpResponse("NO GROUP FOUND")

        else:
            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'accounts/login.html'
    )

def logout_view(request):

    logout(request)

    return redirect('login')
