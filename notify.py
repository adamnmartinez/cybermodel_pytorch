import ssl
import smtplib
import getpass
import environment

SSL_PORT = 465
EMAIL_SERVICE = "smtp.gmail.com"
SENDER_ACCOUNT = environment.sender_email
SENDER_PASSWORD = environment.sender_password
RECIPIENT_ACCOUNT = environment.recipient_email

def send_email_report(entries):
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(EMAIL_SERVICE, SSL_PORT, context=context) as server:
        server.login(SENDER_ACCOUNT, SENDER_PASSWORD)

        message = """Subject: NetLog: Your network traffic report is ready!\n"""
        message += "Here is some flagged traffic you may want to take a look at:\n"

        for entry in entries:
            message += entry
            message += "\n"

        server.sendmail(SENDER_ACCOUNT, RECIPIENT_ACCOUNT, message)

if __name__ == "__main__":
    print("Starting Notification Test...")

    entries = [
        "This is a test entry",
        "This is also a test entry",
        "This too, is a test entry"
    ]

    send_email_report(entries)

    