import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password):
    """
    Send an email with the specified subject and body.
    :param subject: Email subject
    :param body: Email body
    :param to_email: Recipient email address
    :param from_email: Sender email address
    :param smtp_server: SMTP server address
    :param smtp_port: SMTP server port
    :param login: Email login
    :param password: Email password
    :return: None
    """
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    print(from_email)
    print(to_email)
    print(subject)
    print(smtp_server)
    print(smtp_port)
    print(login)

    # Set up the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS
        server.login(login, password)  # Login to the server
        server.send_message(msg)