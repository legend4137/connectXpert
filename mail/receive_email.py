import imaplib
import email
import getpass

def fetch_emails(email_address, password):
  
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    mail.select('inbox')
    
    _, data = mail.search(None, 'FROM "{}"'.format("no-reply@classroom.google.com"))
    email_ids = data[0].split()[::-1]

    for email_id in email_ids:
        _, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        print('From:', msg['From'])
        print('Subject:', msg['Subject'])
        print('Body:', msg.get_payload())

    mail.logout()

def main():
    email_address = input('Enter your email: ')
    password = getpass.getpass('Enter your password: ')

    fetch_emails(email_address, password)

if __name__ == "__main__":
    main()

