import smtplib
from email.mime.text import MIMEText
import utils.emailer_creds as emailer_creds

def send_email(subject:str, body:str, sender:str, recipients:list[str]|str):
    server = emailer_creds.get_smpt_server_of(sender)
    port = emailer_creds.get_smpt_port_of(sender)
    username = emailer_creds.get_smpt_username_of(sender)
    password = emailer_creds.get_smpt_password_of(sender)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients) if type(recipients) == list else recipients
    
    try:
        with smtplib.SMTP_SSL(server, port) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
    except Exception as e:
        print(e)
        return False, "Could not send email"

    return True, "Email sent"