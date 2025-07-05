# Contact Form Email Setup Guide

Your contact form is now configured to send messages to **montebrunce@proton.me**. Here's how to complete the setup:

## Quick Setup

1. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file with your email credentials:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Fill in your SMTP credentials** (see options below)

## Email Provider Options

### Option 1: Gmail (Recommended for testing)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-gmail@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=your-gmail@gmail.com
```

**Setup steps for Gmail:**
1. Enable 2-factor authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an "App Password" for "Mail"
4. Use this App Password (not your regular password) in EMAIL_PASSWORD

### Option 2: Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@outlook.com
EMAIL_PASSWORD=your-password
EMAIL_FROM=your-email@outlook.com
```

### Option 3: ProtonMail (Advanced)
ProtonMail requires ProtonMail Bridge for SMTP access:
```env
EMAIL_HOST=127.0.0.1
EMAIL_PORT=1025
EMAIL_USERNAME=your-email@proton.me
EMAIL_PASSWORD=your-bridge-password
EMAIL_FROM=your-email@proton.me
```

### Option 4: Other SMTP Services
You can use any SMTP service like SendGrid, Mailgun, etc. Just update the HOST and PORT accordingly.

## Testing the Setup

1. **Start your server:**
   ```bash
   python main.py
   ```

2. **Visit the contact page:**
   ```
   http://localhost:8000/contact
   ```

3. **Fill out and submit the form** - you should receive an email at montebrunce@proton.me

## Troubleshooting

### Common Issues:

1. **"Authentication failed" error:**
   - For Gmail: Make sure you're using an App Password, not your regular password
   - Check that 2FA is enabled on your Google account

2. **"Connection refused" error:**
   - Check your EMAIL_HOST and EMAIL_PORT settings
   - Ensure your firewall isn't blocking the connection

3. **"SSL/TLS" errors:**
   - Most providers use port 587 with STARTTLS
   - Some use port 465 with SSL

4. **No email received:**
   - Check spam/junk folder
   - Verify the EMAIL_TO address is correct (montebrunce@proton.me)
   - Check server logs for error messages

### Debug Mode
To see detailed error messages, check the console output when running the server. Email errors will be logged there.

## Security Notes

- Never commit your .env file to version control
- Use App Passwords instead of regular passwords when possible
- In production, consider using a dedicated email service like SendGrid or AWS SES
- The .env file is already in .gitignore to prevent accidental commits

## What Happens Now

When someone submits the contact form:
1. The form data is sent to your FastAPI backend
2. An HTML email is formatted with all the form details
3. The email is sent to montebrunce@proton.me via SMTP
4. The user sees a success/error message

The email will include:
- Name, email, phone, company
- Subject and message
- Formatted in a clean HTML layout
- Clear indication it came from your website contact form
