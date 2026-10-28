from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts_app.demo_accounts import PUBLIC_DEMO_ACCOUNTS


class Command(BaseCommand):
    help = "Create/update only the three public portfolio users; leave group permissions intact."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        groups = {group.name: group for group in Group.objects.filter(
            name__in=[account["role"] for account in PUBLIC_DEMO_ACCOUNTS]
        )}
        if len(groups) != 3:
            raise CommandError("ADMIN, MANAGER and ATTENDANT groups must already be configured.")
        for account in PUBLIC_DEMO_ACCOUNTS:
            user = User.objects.select_for_update().filter(username=account["username"]).first()
            marker = f"{account['label']} Demo"
            if user and (user.is_superuser or user.first_name != "Portfolio" or user.last_name != marker):
                raise CommandError(f"Refusing to overwrite an unrelated account: {account['username']}")
            created = user is None
            if created:
                user = User(username=account["username"], first_name="Portfolio", last_name=marker)
            user.is_active = True
            # ADMIN is an application role, never a public Django staff/superuser.
            user.is_staff = False
            user.is_superuser = False
            if not user.check_password(account["password"]):
                user.set_password(account["password"])
            user.save()
            user.groups.set([groups[account["role"]]])
            user.user_permissions.clear()
            self.stdout.write(f"{'Created' if created else 'Updated'} {user.username} -> {account['role']}")
        self.stdout.write(self.style.SUCCESS("Public demo accounts ready; existing group permissions unchanged."))
