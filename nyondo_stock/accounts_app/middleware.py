from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .demo_accounts import is_demo_user


class DemoAccountProtectionMiddleware(MiddlewareMixin):
    """Keep public demos out of Django administration and credential-changing views."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not is_demo_user(request.user):
            return None
        match = request.resolver_match
        view_class = getattr(view_func, "view_class", None)
        credential_view = view_class and issubclass(
            view_class, (PasswordChangeView, PasswordResetConfirmView)
        )
        if "admin" in match.namespaces or credential_view:
            return HttpResponseForbidden("Public demo accounts cannot manage accounts or change passwords.")
        return None
