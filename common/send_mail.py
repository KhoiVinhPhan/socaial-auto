import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "khoivinhphan@gmail.com"  # Replace with your Gmail
password = "jluu mbeq fgeh dond"  # Replace with your Gmail app password


def send_email(subject, body, receiver_email=None):
    """
    Send an email using Gmail SMTP

    Args:
        subject (str): Email subject
        body (str): Email body content
        sender_email (str): Sender's email address
        receiver_email (list or str): Recipient's email address(es)
        password (str): Gmail app password for authentication
    """
    if receiver_email is None:
        receiver_email = ["vinhppvk@tora-tech.com"]
    elif isinstance(receiver_email, str):
        receiver_email = [receiver_email]

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject

    # Add body
    message.attach(MIMEText(body, "plain"))

    # Create SMTP session and send
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
    finally:
        server.quit()
