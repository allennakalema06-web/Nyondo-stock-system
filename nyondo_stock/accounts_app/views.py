from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib import messages  # type: ignore

# Create your views here.


def login_view(request):

    # Redirect already logged-in users directly to their dashboard
    if request.user.is_authenticated:
        if request.user.groups.filter(name='ADMIN').exists():
            return redirect('admin_dashboard')
        elif request.user.groups.filter(name='MANAGER').exists():
            return redirect('manager_dashboard')
        elif request.user.groups.filter(name='ATTENDANT').exists():
            return redirect('attendant_dashboard')
        else:
            return redirect('access_denied')

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
                return redirect('admin_dashboard')

            elif user.groups.filter(name='MANAGER').exists():
                return redirect('manager_dashboard')

            elif user.groups.filter(name='ATTENDANT').exists():
                return redirect('attendant_dashboard')

            else:
                messages.warning(
                    request,
                    'Your account has no assigned group permissions.'
                )
                return redirect('access_denied')

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