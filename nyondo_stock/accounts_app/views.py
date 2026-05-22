from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

            role = user.userprofile.role.username

            if role == 'ADMIN':
                return redirect('admin_dashboard')

            elif role == 'MANAGER':
                return redirect('manager_dashboard')

            elif role == 'ATTENDANT':
                return redirect('attendant_dashboard')

    return render(request, 'accounts/login.html')

def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def admin_dashboard(request):

    if request.user.userprofile.role.username != 'ADMIN':
        return redirect('login')

    return render(request, 'accounts/admin_dashboard.html')

@login_required
def manager_dashboard(request):

    if request.user.userprofile.role.username != 'MANAGER':
        return redirect('login')

    return render(request, 'manager/manager_dashboard.html')

@login_required
def attendant_dashboard(request):

    if request.user.userprofile.role.username != 'ATTENDANT':
        return redirect('login')

    return render(request, 'accounts/attendant_dashboard.html')