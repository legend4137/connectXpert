import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass

def send_email():
    sender_email = input('Enter your email: ')
    sender_password = getpass.getpass('Enter your password: ')
    recipient_email = input('Enter recipient email address: ')
    subject = input('Enter email subject: ')
    message = input('Enter email message: ')
    attachment = input('Enter attachment file path (press Enter if none): ')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attachment:
        attachment_part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as attachment_file:
            attachment_part.set_payload(attachment_file.read())
        encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', f'attachment; filename= {attachment}')
        msg.attach(attachment_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def main():
    send_email()

if __name__ == "__main__":
    main()