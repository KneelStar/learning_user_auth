import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    # Your email configuration
    smtp_server = 'your_smtp_server'
    smtp_port = 587  # Change to the appropriate port for your SMTP server
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'

    # Create the MIMEText object for the email body
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start the TLS connection (for secure communication)
        server.starttls()

        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, to_email, msg.as_string())

# Example usage:
# subject = 'Test Email'
# body = 'This is a test email sent from Python.'
# to_email = 'recipient@example.com'

# send_email(subject, body, to_email)
