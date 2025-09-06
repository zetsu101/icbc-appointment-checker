"""
Configuration module for ICBC Appointment Checker.
Handles environment variables and application settings.
"""

import os
from datetime import datetime
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for ICBC Appointment Checker."""
    
    # ICBC Login Credentials
    ICBC_LAST_NAME = os.getenv('ICBC_LAST_NAME')
    ICBC_LICENSE_NUMBER = os.getenv("ICBC_LICENSE_NUMBER")
    ICBC_KEYWORD = os.getenv("ICBC_KEYWORD")
    
    # ICBC Booking Preferences
    LICENSE_TYPE = os.getenv('LICENSE_TYPE', 'N')  # N for Novice, 5 for Class 5
    PREFERRED_CITY = os.getenv('PREFERRED_CITY', 'Vancouver')
    EARLIEST_ACCEPTABLE_DATE = os.getenv('EARLIEST_ACCEPTABLE_DATE', '2025-09-03')
    PREFERRED_TEST_CENTERS = os.getenv("PREFERRED_TEST_CENTERS", "Downtown,Richmond,Burnaby,Victoria")
    
    # Notification Settings
    NOTIFICATION_METHOD = os.getenv('NOTIFICATION_METHOD', 'console')
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '10'))
    
    # Email Configuration
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')
    
    # ICBC Website URLs
    ICBC_LOGIN_URL = os.getenv("ICBC_LOGIN_URL", "https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver")
    ICBC_BOOKING_URL = os.getenv('ICBC_BOOKING_URL', 'https://onlinebusiness.icbc.com/web/guest/road-test-booking')
    
    # Browser Configuration
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
    BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', '30'))
    
    @classmethod
    def get_preferred_test_centers(cls) -> List[str]:
        """Get list of preferred test centers."""
        return [center.strip() for center in cls.PREFERRED_TEST_CENTERS.split(',')]
    
    @classmethod
    def get_earliest_acceptable_date(cls) -> datetime:
        """Get earliest acceptable date as datetime object."""
        return datetime.strptime(cls.EARLIEST_ACCEPTABLE_DATE, '%Y-%m-%d')
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        required_fields = [
            "ICBC_KEYWORD",
            'ICBC_LAST_NAME',
            'ICBC_LICENSE_NUMBER'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing required configuration: {', '.join(missing_fields)}")
            return False
        
        # Validate notification method
        if cls.NOTIFICATION_METHOD == 'email':
            email_fields = ['EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT']
            for field in email_fields:
                if not getattr(cls, field):
                    print(f"Email notification requires: {field}")
                    return False
        
        elif cls.NOTIFICATION_METHOD == 'sms':
            sms_fields = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER', 'RECIPIENT_PHONE_NUMBER']
            for field in sms_fields:
                if not getattr(cls, field):
                    print(f"SMS notification requires: {field}")
                    return False
        
        return True
