# Setup Guide - PartyTicket Nigeria

This guide will walk you through setting up all the new features on Railway.

## Step 1: Database Migration

After Railway redeploys with the new code, you need to run a migration to add the new database tables and fields.

### In Railway:

1. Go to your **app service** (not the database service)
2. Click on **Shell/Console** tab
3. Run these commands:

```bash
flask db upgrade
```

This will create:
- `transaction` table (for payment tracking)
- New fields on `user` table (email_verified, email_verification_token, password_reset_token, etc.)
- Updated `ticket` fields (used_at, payment_status improvements)

---

## Step 2: Configure Environment Variables

In Railway, go to your **app service → Variables** and add/update these:

### Email Configuration (Required for ticket emails)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=PartyTicket <your-email@gmail.com>
```

**To get Gmail App Password:**
1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Go to "App passwords"
4. Generate a new app password for "Mail"
5. Use that password (not your regular Gmail password)

### Platform Fee (Your Revenue Share)

```env
PLATFORM_FEE_PERCENT=2.5
```

This is the percentage you take from each ticket sale. Default is 2.5%.

### Existing Variables (Keep These)

Make sure you still have:
- `DATABASE_URL` (from your Postgres service)
- `SECRET_KEY`
- `PAYSTACK_PUBLIC_KEY`
- `PAYSTACK_SECRET_KEY`
- `FLUTTERWAVE_PUBLIC_KEY`
- `FLUTTERWAVE_SECRET_KEY`
- `FLASK_CONFIG=production`
- `FLASK_APP=run.py`

---

## Step 3: Configure Paystack Webhook

This is **critical** for automatic payment processing!

1. Log into your **Paystack Dashboard**
2. Go to **Settings → API Keys & Webhooks**
3. Click **Add Webhook**
4. Enter your Railway app URL:
   ```
   https://your-railway-app-url.railway.app/payment/paystack/webhook
   ```
   (Replace `your-railway-app-url` with your actual Railway domain)
5. Select events: **charge.success**
6. Save the webhook

**Why this matters:** Without the webhook, payments won't automatically create tickets. Users would have to manually verify payments.

---

## Step 4: Test the Flow

### Test Email Verification:

1. Register a new account
2. Check your email (or the email you configured)
3. Click the verification link
4. You should be able to login

### Test Password Reset:

1. Go to login page
2. Click "Forgot your password?"
3. Enter your email
4. Check email for reset link
5. Click link and set new password

### Test Ticket Purchase:

1. Create an event (or use existing one)
2. Click "Get Tickets"
3. Select quantity
4. Click "Pay with Paystack"
5. Complete test payment (use Paystack test card: `4084084084084081`)
6. After payment, you should:
   - Be redirected back to event page
   - Receive confirmation email with QR code
   - See tickets in your dashboard

### Test Ticket Verification:

1. After purchasing a ticket, you'll get a QR code
2. Use the API endpoint to verify:
   ```bash
   POST /api/verify_ticket
   {
     "ticket_id": 123
   }
   ```
3. First scan should succeed
4. Second scan should fail (fraud protection)

---

## Step 5: Monitor Transactions

You can now track all payments in the `transaction` table:

- `amount`: Total paid by customer
- `platform_fee`: Your cut (2.5% by default)
- `organizer_amount`: What the event organizer gets
- `status`: Payment status (initialized, pending, success, failed)

---

## Troubleshooting

### Emails not sending?

- Check `MAIL_USERNAME` and `MAIL_PASSWORD` are correct
- Make sure you're using an **App Password** for Gmail, not your regular password
- Check Railway logs for email errors

### Payments not creating tickets?

- Verify Paystack webhook is configured correctly
- Check webhook URL matches your Railway domain
- Check Railway logs for webhook errors
- Make sure `PAYSTACK_SECRET_KEY` is set correctly (webhook signature verification)

### Database errors?

- Make sure you ran `flask db upgrade` in Railway shell
- Check that `DATABASE_URL` is set correctly
- Verify Postgres service is running

### Can't login after registration?

- Check if email verification is required (it should be)
- Look for verification email in spam folder
- You can manually verify in database if needed (set `email_verified = true`)

---

## What's New?

✅ **Real Payment Processing**: Payments now create transactions with platform fees  
✅ **Email Verification**: Users must verify email before full access  
✅ **Password Reset**: Secure password reset flow  
✅ **Beautiful Email Templates**: Professional ticket confirmation emails  
✅ **Fraud Protection**: Tickets can only be used once  
✅ **Organizer Notifications**: Alerts when events sell well  

---

## Need Help?

Check Railway logs for detailed error messages. Most issues are:
- Missing environment variables
- Incorrect email configuration
- Webhook not configured
- Database migration not run

