# DAO para usuario
class UserDAO:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_user_by_username(self, username):
        cursor = self.mysql.connection.cursor()
        query = "SELECT id_usuario, nombre_usuario, contrasenia_usuario FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user