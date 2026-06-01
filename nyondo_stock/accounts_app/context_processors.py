def user_roles(request):
    user = request.user

    if not user.is_authenticated:
        return {
            "is_admin": False,
            "is_manager": False,
            "is_attendant": False,
        }

    groups = user.groups.values_list("name", flat=True)

    return {
        "is_admin": "ADMIN" in groups,
        "is_manager": "MANAGER" in groups or "ADMIN" in groups,
        "is_attendant": "ATTENDANT" in groups or "ADMIN" in groups,
    }