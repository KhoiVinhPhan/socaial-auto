import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "khoivinhphan@gmail.com"  # Replace with your Gmail
password = "jluu mbeq fgeh dond"  # Replace with your Gmail app password


def send_email(subject, body, receiver_email="vinhppvk@tora-tech.com"):
    """
    Send an email using Gmail SMTP
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        sender_email (str): Sender's email address
        receiver_email (str): Recipient's email address 
        password (str): Gmail app password for authentication
    """
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
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
