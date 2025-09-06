
#!/usr/bin/env python3
"""
Test script to verify ICBC Appointment Checker setup.
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from notifier import Notifier


def test_configuration():
    """Test configuration loading and validation."""
    print("Testing configuration...")
    
    # Test basic config loading
    try:
        config = Config()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False
    
    # Test required fields
    required_fields = ['ICBC_LAST_NAME', 'ICBC_LICENSE_NUMBER']
    missing_fields = []
    
    for field in required_fields:
        if not getattr(config, field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"⚠️  Missing required fields: {', '.join(missing_fields)}")
        print("   Please add these to your .env file")
    else:
        print("✅ All required fields present")
    
    # Test notification method validation
    if config.NOTIFICATION_METHOD == 'email':
        email_fields = ['EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT']
        missing_email = [field for field in email_fields if not getattr(config, field)]
        if missing_email:
            print(f"⚠️  Email notification requires: {', '.join(missing_email)}")
        else:
            print("✅ Email configuration complete")
    
    elif config.NOTIFICATION_METHOD == 'sms':
        sms_fields = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER', 'RECIPIENT_PHONE_NUMBER']
        missing_sms = [field for field in sms_fields if not getattr(config, field)]
        if missing_sms:
            print(f"⚠️  SMS notification requires: {', '.join(missing_sms)}")
        else:
            print("✅ SMS configuration complete")
    
    elif config.NOTIFICATION_METHOD == 'console':
        print("✅ Console notification configured")
    
    return True


def test_notifier():
    """Test notification system."""
    print("\nTesting notification system...")
    
    try:
        notifier = Notifier()
        print("✅ Notifier initialized successfully")
    except Exception as e:
        print(f"❌ Notifier initialization failed: {e}")
        return False
    
    # Test notification with sample data
    test_appointment = {
        'date': '2024-02-15',
        'time': '10:30 AM',
        'location': 'Downtown ICBC Office',
        'license_type': Config.LICENSE_TYPE
    }
    
    try:
        success = notifier.send_notification(test_appointment)
        if success:
            print("✅ Test notification sent successfully")
        else:
            print("❌ Test notification failed")
            return False
    except Exception as e:
        print(f"❌ Test notification error: {e}")
        return False
    
    return True


def test_dependencies():
    """Test if all required dependencies are installed."""
    print("\nTesting dependencies...")
    
    # Map package names (as in requirements.txt) to their importable module names
    required_packages = {
        'selenium': 'selenium',
        'beautifulsoup4': 'bs4',
        'requests': 'requests',
        'python-dotenv': 'dotenv',
        'schedule': 'schedule'
    }
    
    if Config.NOTIFICATION_METHOD == 'sms':
        required_packages['twilio'] = 'twilio'
    
    missing_packages = []
    
    for package, module_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Run all tests."""
    print("="*50)
    print("ICBC Appointment Checker - Setup Test")
    print("="*50)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Notifier", test_notifier)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("You can now run: python main.py --test")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
