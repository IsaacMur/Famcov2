from flask_mysqldb import MySQL  # type: ignore

def init_db(app):
    app.config['MYSQL_HOST'] = 'dpg-ctf1bpbtq21c73bqfub0-a'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'JaoCzQoZye5wHW8O1Qpu1LcS61JIFmFD'
    app.config['MYSQL_DB'] = 'famco'
    return MySQL(app)
