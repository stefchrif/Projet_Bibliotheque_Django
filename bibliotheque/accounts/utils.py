def is_bibliothecaire(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'bibliothecaire'
