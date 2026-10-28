"""Exercise the running app against Neon; remove all temporary test records."""
import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "nyondo_stock"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nyondo_stock.settings")
import django
django.setup()
import requests
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from django.db import connection
from inventory_app.models import Category

assert connection.vendor == "postgresql"
assert ".neon.tech" in settings.DATABASES["default"]["HOST"], "Expected Neon database"
base = "http://127.0.0.1:8000"
tag = "neon_smoke_" + secrets.token_hex(6)
password = secrets.token_urlsafe(32)
user = None
group = None
group_created = False
session_key = None
client = requests.Session()
def get(path):
    response = client.get(base + path, timeout=30)
    response.raise_for_status()
    return response
def post(path, data):
    get(path)
    data = {**data, "csrfmiddlewaretoken": client.cookies["csrftoken"]}
    response = client.post(base + path, data=data, headers={"Referer": base + path}, timeout=30, allow_redirects=False)
    assert response.status_code == 302, (path, response.status_code)
    return response
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
    print("PASS: Neon PostgreSQL query")
    group, group_created = Group.objects.get_or_create(name="MANAGER")
    user = User.objects.create_user(username=tag, password=password)
    user.groups.add(group)
    response = post("/login/", {"username": tag, "password": password})
    assert response.headers["Location"] == "/manager_dashboard/"
    session_key = client.cookies[settings.SESSION_COOKIE_NAME]
    assert Session.objects.get(session_key=session_key).get_decoded()["_auth_user_id"] == str(user.pk)
    print("PASS: HTTP login and session persisted in Neon")
    assert get("/manager_dashboard/").status_code == 200
    print("PASS: authenticated manager dashboard HTTP 200")
    post("/add_category/", {"category_name": tag})
    category = Category.objects.get(category_name=tag)
    assert tag in get("/categories/").text
    print("PASS: HTTP create category, Neon persistence, HTTP list read")
    updated = tag + "_updated"
    post(f"/edit_category/{category.pk}/", {"category_name": updated})
    category.refresh_from_db()
    assert category.category_name == updated
    assert updated in get("/categories/").text
    print("PASS: HTTP update category persisted and rendered")
    post(f"/delete_category/{category.pk}/", {})
    assert not Category.objects.filter(pk=category.pk).exists()
    print("PASS: HTTP delete category removed Neon row")
finally:
    Category.objects.filter(category_name__in=[tag, tag + "_updated"]).delete()
    if session_key:
        Session.objects.filter(session_key=session_key).delete()
    if user:
        user.delete()
    if group_created:
        group.delete()
    client.close()
    connection.close()
    print("Temporary smoke-test records cleaned up")
