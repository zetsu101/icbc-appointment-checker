#!/usr/bin/env python3
"""
Main entry point for ICBC Appointment Checker.
Orchestrates the appointment checking process.
"""

import sys
import argparse
from datetime import datetime

from config import Config
from icbc_checker import ICBCAppointmentChecker


def main():
    """Main function to run the ICBC appointment checker."""
    parser = argparse.ArgumentParser(description='ICBC Appointment Checker')
    parser.add_argument('--once', action='store_true', 
                       help='Check appointments once and exit')
    parser.add_argument('--continuous', action='store_true', 
                       help='Check appointments continuously (default)')
    parser.add_argument('--test', action='store_true', 
                       help='Run in test mode with sample data')
    
    args = parser.parse_args()
    
    # Validate configuration
    if not Config.validate_config():
        print("Configuration validation failed. Please check your .env file.")
        sys.exit(1)
    
    # Create checker instance
    checker = ICBCAppointmentChecker()
    
    print("="*60)
    print("🚗 ICBC Appointment Checker")
    print("="*60)
    print(f"License Type: {Config.LICENSE_TYPE}")
    print(f"Preferred City: {Config.PREFERRED_CITY}")
    print(f"Test Centers: {', '.join(Config.get_preferred_test_centers())}")
    print(f"Earliest Acceptable Date: {Config.EARLIEST_ACCEPTABLE_DATE}")
    print(f"Notification Method: {Config.NOTIFICATION_METHOD}")
    print(f"Check Interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
    print("="*60)
    
    if args.test:
        run_test_mode(checker)
    elif args.once:
        run_single_check(checker)
    else:
        run_continuous_check(checker)


def run_single_check(checker: ICBCAppointmentChecker):
    """Run a single appointment check."""
    print("\nRunning single appointment check...")
    success = checker.check_for_new_appointments()
    
    if success:
        print("Appointment check completed successfully")
    else:
        print("Appointment check failed")
        sys.exit(1)


def run_continuous_check(checker: ICBCAppointmentChecker):
    """Run continuous appointment checking."""
    print("\nStarting continuous appointment checking...")
    checker.run_continuous_check()


def run_test_mode(checker: ICBCAppointmentChecker):
    """Run in test mode with sample data."""
    print("\nRunning in test mode...")
    
    # Sample appointment data for testing
    test_appointment = {
        'date': '2024-02-15',
        'time': '10:30 AM',
        'location': 'Downtown ICBC Office',
        'license_type': Config.LICENSE_TYPE
    }
    
    print("Sending test notification...")
    success = checker.notifier.send_notification(test_appointment)
    
    if success:
        print("Test notification sent successfully")
    else:
        print("Test notification failed")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAppointment checker stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
