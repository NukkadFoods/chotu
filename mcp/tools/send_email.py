# mcp/tools/send_email.py
import smtplib
import email

def send_email(recipient_email, subject, body):
    """
    Sends an email to the specified recipient with the given subject and body
    
    Args:
        recipient_email: Email address of the recipient
        subject: Subject of the email
        body: Body of the email
    
    Returns:
        str: Success/error message
    """
    try:
        # Implementation here
        server = smtplib.SMTP('localhost')
        message = email.message.EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = 'sender@example.com'
        message['To'] = recipient_email
        
        server.send_message(message)
        server.quit()
        
        return "✅ Email sent successfully"
    except Exception as e:
        return f"❌ Error: {e}"