from io import StringIO
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import PasswordChangeView
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import include, path
from .demo_accounts import PUBLIC_DEMO_ACCOUNTS

urlpatterns = [path("", include("nyondo_stock.urls")), path("test-password-change/", PasswordChangeView.as_view())]

class DemoAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for account in PUBLIC_DEMO_ACCOUNTS:
            group = Group.objects.create(name=account["role"])
            group.permissions.add(Permission.objects.get(content_type__app_label="inventory_app", codename="view_product"))
        cls.allen = get_user_model().objects.create_superuser("allen", password="private-test-only")

    def seed(self):
        call_command("seed_demo_accounts", stdout=StringIO())

    def test_seed_idempotency_and_preserves_personal_admin_and_permissions(self):
        before = get_user_model().objects.values().get(pk=self.allen.pk)
        permissions = list(Group.permissions.through.objects.order_by("id").values())
        self.seed()
        hashes = {u.username: u.password for u in get_user_model().objects.exclude(pk=self.allen.pk)}
        self.seed()
        self.assertEqual(get_user_model().objects.count(), 4)
        self.assertEqual(before, get_user_model().objects.values().get(pk=self.allen.pk))
        self.assertEqual(permissions, list(Group.permissions.through.objects.order_by("id").values()))
        for account in PUBLIC_DEMO_ACCOUNTS:
            user = get_user_model().objects.get(username=account["username"])
            self.assertTrue(user.check_password(account["password"]))
            self.assertEqual(user.password, hashes[user.username])
            self.assertTrue(user.is_active)
            self.assertFalse(user.is_staff or user.is_superuser)
            self.assertEqual(list(user.groups.values_list("name", flat=True)), [account["role"]])
            self.assertFalse(user.user_permissions.exists())

    def test_seed_refuses_unrelated_existing_account(self):
        get_user_model().objects.create_user("demo_admin", password="private-existing-test")
        with self.assertRaises(CommandError): self.seed()
        self.assertFalse(get_user_model().objects.filter(username="demo_manager").exists())

    @override_settings(ROOT_URLCONF="accounts_app.tests")
    def test_role_login_dashboards_and_server_side_restrictions(self):
        self.seed()
        dashboards = {"ADMIN": "/admin_dashboard/", "MANAGER": "/manager_dashboard/", "ATTENDANT": "/attendant_dashboard/"}
        allowed = {"ADMIN": set(dashboards), "MANAGER": {"MANAGER"}, "ATTENDANT": {"ATTENDANT"}}
        for account in PUBLIC_DEMO_ACCOUNTS:
            with self.subTest(role=account["role"]):
                self.client.logout()
                response = self.client.post("/login/", {"username": account["username"], "password": account["password"]})
                self.assertRedirects(response, dashboards[account["role"]])
                for role, url in dashboards.items():
                    response = self.client.get(url)
                    if role in allowed[account["role"]]: self.assertEqual(response.status_code, 200)
                    else: self.assertRedirects(response, "/access_denied/", target_status_code=403)
                for url in ["/admin/", "/admin/auth/user/", "/admin/password_change/", "/test-password-change/"]:
                    self.assertEqual(self.client.get(url).status_code, 403)
                    self.assertEqual(self.client.post(url, {}).status_code, 403)

    def test_public_page_buttons_and_manual_fallback(self):
        response = self.client.get("/login/")
        self.assertContains(response, "Try the demo")
        self.assertContains(response, "<details")
        self.assertContains(response, 'type="button"', count=3)
        for account in PUBLIC_DEMO_ACCOUNTS:
            self.assertContains(response, account["username"])
            self.assertContains(response, account["password"])
        self.assertNotContains(response, settings.SECRET_KEY)
        self.assertNotContains(response, "private-test-only")

    def test_invalid_login_feedback(self):
        response = self.client.post("/login/", {"username": "missing", "password": "incorrect"})
        self.assertContains(response, "Invalid username or password")
