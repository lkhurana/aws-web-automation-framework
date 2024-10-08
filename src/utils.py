import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
from botocore.exceptions import ClientError
from src.config import REGION_NAME

def send_email(subject, body, to_email, smtp_server, smtp_port, login, password):
    """
    Sends an email with the specified subject and body.

    This function sets up the SMTP server connection, logs in using provided
    credentials, and sends an email to the specified recipient.

    Args:
        subject (str): The subject line of the email.
        body (str): The main content of the email.
        to_email (str): The recipient's email address.
        smtp_server (str): The address of the SMTP server.
        smtp_port (int): The port used by the SMTP server.
        login (str): The login username for the email account.
        password (str): The login password for the email account.

    Returns:
        None
    """
    msg = MIMEMultipart()
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS
        server.login(login, password)  # Login to the server
        server.send_message(msg)

def get_credential(parameter_name):
    """
    Fetch a credential from the AWS Systems Manager Parameter Store.

    This function retrieves the value of a parameter stored in the AWS Parameter Store.
    If the parameter is a secure string, it will be decrypted before being returned.

    Args:
        parameter_name (str): The name of the parameter in the Parameter Store.

    Returns:
        str: The value of the parameter (e.g., password or token).

    Raises:
        botocore.exceptions.ClientError: If the parameter does not exist or if there 
                                          are issues fetching it from AWS.
    """
    ssm = boto3.client('ssm', region_name=REGION_NAME)
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']