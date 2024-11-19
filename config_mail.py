import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor de correo
SMTP_SERVER = 'mail.edgecloud.com.mx'
SMTP_PORT = 465
EMAIL = 'contacto@edgecloud.com.mx'
PASSWORD = 'Operaciones1'

def send_email(to_email, subject, message, is_html=False):
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))

        # Conectar al servidor SMTP con SSL
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        return "Correo enviado exitosamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"

