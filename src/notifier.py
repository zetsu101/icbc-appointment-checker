"""
Notification module for ICBC Appointment Checker.
Handles email, SMS, and console notifications.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

from config import Config


class Notifier:
    """Handles different types of notifications."""
    
    def __init__(self):
        self.config = Config()
    
    def send_notification(self, appointment_data: Dict[str, Any]) -> bool:
        """
        Send notification based on configured method.
        
        Args:
            appointment_data: Dictionary containing appointment details
            
        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        try:
            if self.config.NOTIFICATION_METHOD == 'email':
                return self._send_email_notification(appointment_data)
            elif self.config.NOTIFICATION_METHOD == 'sms':
                return self._send_sms_notification(appointment_data)
            elif self.config.NOTIFICATION_METHOD == 'console':
                return self._send_console_notification(appointment_data)
            else:
                print(f"Unknown notification method: {self.config.NOTIFICATION_METHOD}")
                return False
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def _send_email_notification(self, appointment_data: Dict[str, Any]) -> bool:
        """Send email notification."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config.EMAIL_SENDER
            msg['To'] = self.config.EMAIL_RECIPIENT
            msg['Subject'] = "🚗 ICBC Appointment Available!"
            
            # Create email body
            body = self._create_email_body(appointment_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.EMAIL_SENDER, self.config.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(self.config.EMAIL_SENDER, self.config.EMAIL_RECIPIENT, text)
            server.quit()
            
            print(f"Email notification sent to {self.config.EMAIL_RECIPIENT}")
            return True
            
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
    
    def _send_sms_notification(self, appointment_data: Dict[str, Any]) -> bool:
        """Send SMS notification via Twilio."""
        try:
            client = Client(self.config.TWILIO_ACCOUNT_SID, self.config.TWILIO_AUTH_TOKEN)
            
            message_body = self._create_sms_body(appointment_data)
            
            message = client.messages.create(
                body=message_body,
                from_=self.config.TWILIO_PHONE_NUMBER,
                to=self.config.RECIPIENT_PHONE_NUMBER
            )
            
            print(f"SMS notification sent to {self.config.RECIPIENT_PHONE_NUMBER}")
            return True
            
        except TwilioException as e:
            print(f"Twilio error sending SMS: {e}")
            return False
        except Exception as e:
            print(f"Error sending SMS notification: {e}")
            return False
    
    def _send_console_notification(self, appointment_data: Dict[str, Any]) -> bool:
        """Send console notification."""
        try:
            print("\n" + "="*50)
            print("🚗 ICBC APPOINTMENT AVAILABLE!")
            print("="*50)
            print(f"Date: {appointment_data.get('date', 'Unknown')}")
            print(f"Time: {appointment_data.get('time', 'Unknown')}")
            print(f"Location: {appointment_data.get('location', 'Unknown')}")
            print(f"License Type: {appointment_data.get('license_type', 'Unknown')}")
            print(f"Found at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50)
            print("Book your appointment now!")
            print("="*50 + "\n")
            return True
            
        except Exception as e:
            print(f"Error sending console notification: {e}")
            return False
    
    def _create_email_body(self, appointment_data: Dict[str, Any]) -> str:
        """Create HTML email body."""
        return f"""
        <html>
        <body>
            <h2 style="color: #2E8B57;">🚗 ICBC Appointment Available!</h2>
            <p>Great news! An ICBC road test appointment has become available:</p>
            
            <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Date:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{appointment_data.get('date', 'Unknown')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Time:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{appointment_data.get('time', 'Unknown')}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Location:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{appointment_data.get('location', 'Unknown')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>License Type:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{appointment_data.get('license_type', 'Unknown')}</td>
                </tr>
            </table>
            
            <p><strong>Found at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <p style="color: #FF6B6B; font-weight: bold;">⚠️ Book your appointment quickly before it's taken!</p>
            
            <p>
                <a href="{self.config.ICBC_BOOKING_URL}" 
                   style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">
                    Book Appointment Now
                </a>
            </p>
            
            <hr>
            <p style="font-size: 12px; color: #666;">
                This notification was sent by ICBC Appointment Checker.<br>
                For educational purposes only. Please respect ICBC's terms of service.
            </p>
        </body>
        </html>
        """
    
    def _create_sms_body(self, appointment_data: Dict[str, Any]) -> str:
        """Create SMS message body."""
        return f"""🚗 ICBC Appointment Available!
Date: {appointment_data.get('date', 'Unknown')}
Time: {appointment_data.get('time', 'Unknown')}
Location: {appointment_data.get('location', 'Unknown')}
License: {appointment_data.get('license_type', 'Unknown')}
Book now: {self.config.ICBC_BOOKING_URL}"""
