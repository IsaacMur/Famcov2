from flask import session, flash, redirect, url_for

class UserViewModel:
    def __init__(self, user_cqrs):
        self.user_cqrs = user_cqrs

    def login_user(self, username, password):
        is_authenticated, user = self.user_cqrs.authenticate_user(username, password)
        if is_authenticated:
            session['username'] = user['nombre_usuario']  # Guarda el nombre de usuario en la sesión
            flash('Inicio de sesión exitoso', 'success')
            return True
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')
            return False
