from blog.schema import UserProfileSchema
from blog.services import UserService, UserNotFound

def connected_user(user_id):
    """
    Retourne le schema de l'utilisateur connecté.
    """
    if user_id == None:
        return None

    try:
        user = UserService.get_user_by_id(user_id)
        user_schema = UserProfileSchema()
        return user_schema.dump(user)
    except UserNotFound as e:
        return None