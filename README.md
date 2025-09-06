# ICBC Appointment Checker

🚗 **Automated ICBC Road Test Appointment Monitor**

A Python-based automation tool that monitors the ICBC (Insurance Corporation of British Columbia) road test booking system for earlier appointment openings and sends alerts when available.

## 🎯 Problem Statement

ICBC road test appointments are notoriously difficult to book due to high demand and limited availability. Cancellations happen frequently but are snatched up quickly, making it nearly impossible to catch them manually. This tool automates the monitoring process to help you secure an earlier appointment.

## ✨ Features

- **Automated Login**: Securely logs into your ICBC account
- **Smart Monitoring**: Checks for available appointments based on your preferences
- **Multiple Notification Methods**:
  - 📧 Email notifications (Gmail)
  - 📱 SMS notifications (Twilio)
  - 💻 Console output (for testing)
- **Flexible Scheduling**: Runs every 5-15 minutes (configurable)
- **Preference Filtering**: Only alerts for appointments that meet your criteria
- **Multiple Deployment Options**: Local, GitHub Actions, or cloud platforms

## 🛠️ Tech Stack

- **Python 3.11+**
- **Selenium** - Browser automation
- **BeautifulSoup** - HTML parsing
- **Twilio** - SMS notifications
- **SMTP** - Email notifications
- **GitHub Actions** - Automated scheduling

## 📋 Prerequisites

- Python 3.11 or higher
- Chrome browser installed
- ICBC online account credentials
- (Optional) Twilio account for SMS notifications
- (Optional) Gmail account for email notifications

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/icbc-appointment-checker.git
cd icbc-appointment-checker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your credentials and preferences:

```env
# Required: ICBC Login Credentials
ICBC_USERNAME=your_icbc_username
ICBC_PASSWORD=your_icbc_password

# Required: Booking Preferences
LICENSE_TYPE=N  # N for Novice, 5 for Class 5
PREFERRED_CITY=Vancouver
EARLIEST_ACCEPTABLE_DATE=2024-01-01
PREFERRED_TEST_CENTERS=Downtown,Richmond,Burnaby

# Required: Notification Settings
NOTIFICATION_METHOD=console  # email, sms, or console
CHECK_INTERVAL_MINUTES=10

# Optional: Email Configuration (if using email notifications)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=your_email@gmail.com

# Optional: Twilio Configuration (if using SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
RECIPIENT_PHONE_NUMBER=+1234567890
```

### 4. Test the Setup

Run a test to verify your configuration:

```bash
cd src
python main.py --test
```

### 5. Run the Checker

**Single Check:**
```bash
python main.py --once
```

**Continuous Monitoring:**
```bash
python main.py --continuous
```

## 🔧 Configuration Options

### License Types
- `N` - Novice license
- `5` - Class 5 license

### Notification Methods
- `console` - Output to terminal (default)
- `email` - Send email notifications
- `sms` - Send SMS notifications via Twilio

### Test Centers
Specify your preferred test centers as a comma-separated list:
```
PREFERRED_TEST_CENTERS=Downtown,Richmond,Burnaby,North Vancouver
```

## 🚀 Deployment Options

### Option 1: Local Machine (Recommended for Testing)

1. Install dependencies and configure `.env`
2. Run with cron job for automation:

```bash
# Add to crontab (check every 10 minutes)
*/10 * * * * cd /path/to/icbc-appointment-checker/src && python main.py --once
```

### Option 2: GitHub Actions (Recommended for Production)

1. Fork this repository
2. Add your secrets to GitHub repository settings:
   - Go to Settings → Secrets and variables → Actions
   - Add all environment variables from your `.env` file
3. The workflow will run automatically every 10 minutes

### Option 3: Cloud Platforms

#### Heroku
```bash
# Create Procfile
echo "worker: cd src && python main.py --continuous" > Procfile

# Deploy
heroku create your-app-name
heroku config:set ICBC_USERNAME=your_username
heroku config:set ICBC_PASSWORD=your_password
# ... set other environment variables
git push heroku main
```

#### Railway
1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Deploy automatically

## 📧 Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `EMAIL_PASSWORD`

## 📱 SMS Setup (Twilio)

1. Create a Twilio account at [twilio.com](https://www.twilio.com)
2. Get your Account SID and Auth Token from the dashboard
3. Purchase a phone number
4. Add credentials to your `.env` file

## 🔍 Troubleshooting

### Common Issues

**"Chrome WebDriver setup failed"**
- Ensure Chrome is installed
- Try running without headless mode: `HEADLESS_MODE=false`

**"Login failed"**
- Verify your ICBC credentials
- Check if ICBC website is accessible
- Try running manually first to ensure credentials work

**"No appointments found"**
- Check if the website structure has changed
- Verify your preferences are correct
- Try different test centers

**"Email/SMS not sending"**
- Verify your credentials
- Check firewall/network settings
- Test with console notifications first

### Debug Mode

Run with debug output:
```bash
HEADLESS_MODE=false python main.py --once
```

## 📝 Logs

The application provides detailed logging:
- Login attempts and success/failure
- Appointment search results
- Notification delivery status
- Error messages and stack traces

## ⚠️ Important Disclaimers

### Educational Purpose Only
This tool is created for **educational purposes only**. Please respect ICBC's terms of service and website usage policies.

### Rate Limiting
- The tool includes built-in delays to avoid overwhelming ICBC's servers
- Respect reasonable usage patterns
- Do not run multiple instances simultaneously

### Legal Compliance
- Ensure compliance with ICBC's terms of service
- Do not use for commercial purposes
- Respect website robots.txt and usage policies

### Security
- Never commit your `.env` file to version control
- Use strong, unique passwords
- Regularly update your credentials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ICBC for providing the booking system
- Selenium team for browser automation tools
- Twilio for SMS services
- GitHub for Actions automation

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub with detailed information

---

**Remember**: This tool is for educational purposes. Please use responsibly and respect ICBC's terms of service.
