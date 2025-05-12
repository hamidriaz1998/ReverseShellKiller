import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


def send_email_notification(pid, cmdline, confidence):
    """
    Sends an email notification when a reverse shell is detected.

    Args:
        pid (int): Process ID of the detected reverse shell.
        cmdline (list): Command line arguments of the process.
        confidence (float): Confidence score of the detection.
    """
    load_dotenv()
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    recipient_email = os.environ.get("EMAIL_RECIPIENT")
    print(f"Sender email: {sender_email}")
    print(f"Sender password: {sender_password}")
    print(f"Recipient email: {recipient_email}")

    if not sender_email or not sender_password or not recipient_email:
        print(
            "Email credentials or recipient email are not set in the environment variables."
        )
        return

    subject = f"Reverse Shell Detected: PID {pid}"
    body = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f8f8;
        }}
        .container {{
            background-color: #fff;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background-color: #d32f2f;
            color: white;
            padding: 15px;
            margin: -25px -25px 20px -25px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .alert-icon {{
            font-size: 40px;
            margin-bottom: 10px;
        }}
        h2 {{
            margin-top: 0;
            color: white;
        }}
        ul {{
            background-color: #f5f5f5;
            padding: 15px 15px 15px 40px;
            border-radius: 5px;
            border-left: 4px solid #d32f2f;
        }}
        li {{
            padding: 8px 0;
        }}
        .confidence-high {{
            color: #d32f2f;
            font-weight: bold;
        }}
        .confidence-medium {{
            color: #ff9800;
            font-weight: bold;
        }}
        .confidence-low {{
            color: #2196f3;
            font-weight: bold;
        }}
        .action {{
            margin-top: 25px;
            padding: 15px;
            background-color: #ffebee;
            border-radius: 5px;
            border-left: 4px solid #d32f2f;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 12px;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="alert-icon">⚠️</div>
            <h2>SECURITY ALERT: Reverse Shell Detected</h2>
        </div>
        
        <p>A potential reverse shell has been detected on your system. This may indicate an unauthorized access attempt.</p>
        
        <h3>Detection Details:</h3>
        <ul>
            <li><strong>Process ID:</strong> {pid}</li>
            <li><strong>Command:</strong> <code>{
        " ".join(cmdline) if isinstance(cmdline, list) else cmdline
    }</code></li>
            <li><strong>Confidence Score:</strong> 
                {
        f'<span class="confidence-high">{confidence:.2f}</span>'
        if confidence is not None and confidence > 0.7
        else f'<span class="confidence-medium">{confidence:.2f}</span>'
        if confidence is not None and confidence > 0.4
        else f'<span class="confidence-low">{confidence:.2f}</span>'
        if confidence is not None
        else "N/A"
    }
            </li>
            <li><strong>Timestamp:</strong> {
        __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }</li>
        </ul>
        
        <div class="action">
            <p>🚨 IMMEDIATE ACTION IS REQUIRED 🚨</p>
            <p>The suspicious process has been automatically terminated. However, your system may still be compromised.</p>
            <p>Recommended steps:</p>
            <ol>
                <li>Investigate network connections</li>
                <li>Check for unauthorized users</li>
                <li>Scan for malware</li>
                <li>Review system logs</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>This is an automated security alert from your Reverse Shell Detection System.</p>
            <p>Report generated on {
        __import__("datetime").datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
    }</p>
        </div>
    </div>
</body>
</html>
"""
    # Create the email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach HTML content
    msg.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email notification sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
