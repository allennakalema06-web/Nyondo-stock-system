from django.shortcuts import redirect
from functools import wraps

def allowed_roles(allowed_roles=[]):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            user_groups = request.user.groups.values_list('name', flat=True)

            if not any(group in allowed_roles for group in user_groups):
                return redirect('access_denied')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator