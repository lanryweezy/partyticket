# Quick Start Guide

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .flaskenv.example .flaskenv
   # Edit .flaskenv with your configuration
   ```

3. **Initialize database:**
   ```bash
   flask db upgrade
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Access the app:**
   Open http://localhost:5000 in your browser

## Production Deployment

### Quick Deploy to Heroku

1. **Install Heroku CLI** and login
2. **Create app:**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set PAYSTACK_PUBLIC_KEY=your-key
   heroku config:set PAYSTACK_SECRET_KEY=your-key
   heroku config:set FLUTTERWAVE_PUBLIC_KEY=your-key
   heroku config:set FLUTTERWAVE_SECRET_KEY=your-key
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   heroku run flask db upgrade
   ```

### Quick Deploy to Railway

1. Connect your GitHub repository
2. Add environment variables in dashboard
3. Add PostgreSQL service
4. Deploy automatically

## Environment Variables Required

- `SECRET_KEY` - Flask secret key (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL` - PostgreSQL connection string (for production)
- `PAYSTACK_PUBLIC_KEY` - Paystack public key
- `PAYSTACK_SECRET_KEY` - Paystack secret key
- `FLUTTERWAVE_PUBLIC_KEY` - Flutterwave public key
- `FLUTTERWAVE_SECRET_KEY` - Flutterwave secret key

## First Time Setup

1. Create a superuser/admin account by running:
   ```python
   python
   >>> from app import create_app, db
   >>> from app.models import User
   >>> app = create_app()
   >>> with app.app_context():
   ...     user = User(username='admin', email='admin@example.com')
   ...     user.set_password('your-password')
   ...     db.session.add(user)
   ...     db.session.commit()
   ```

## Testing Payment Integration

Use test keys from Paystack/Flutterwave for development. Test cards:
- **Paystack**: 4084084084084081
- **Flutterwave**: 5531886652142950

## Support

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)


