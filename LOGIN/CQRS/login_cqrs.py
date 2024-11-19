from werkzeug.security import check_password_hash

class UserCQRS:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def authenticate_user(self, username, password):
        user = self.user_dao.get_user_by_username(username)
        if user and check_password_hash(user['contrasenia_usuario'], password):
            return True, user
        return False, None
