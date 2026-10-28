"""Intentionally public portfolio credentials. Never put personal secrets here.

After changing these demo-only passwords, run: python manage.py seed_demo_accounts
The login page and seeder share this single source of truth.
"""
PUBLIC_DEMO_ACCOUNTS = ({'label': 'Admin',
  'role': 'ADMIN',
  'username': 'demo_admin',
  'password': 'pR9i7RxUqpS47joNOTmSiGRp'},
 {'label': 'Manager',
  'role': 'MANAGER',
  'username': 'demo_manager',
  'password': 'uNxnyEdMF4qS0R4CPNn5VCHJ'},
 {'label': 'Attendant',
  'role': 'ATTENDANT',
  'username': 'demo_attendant',
  'password': 'c1oxTHHBiHgHxfykaPSdViZM'})

DEMO_USERNAMES = frozenset(account["username"] for account in PUBLIC_DEMO_ACCOUNTS)


def is_demo_user(user):
    return user.is_authenticated and user.get_username() in DEMO_USERNAMES
