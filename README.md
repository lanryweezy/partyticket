# PartyTicket Nigeria

PartyTicket Nigeria is a comprehensive event ticketing and invitation platform designed specifically for the Nigerian market. It enables users to discover, book, and host events ranging from formal gatherings to street parties, concerts, and campus events.

## Features

### Event Management
- **Multi-category Support**: Formal events, campus parties, street parties, concerts, and festivals
- **Event Creation**: Easy-to-use interface for creating and managing events
- **Ticket Sales**: Integrated ticketing system with secure payment processing
- **Invitation System**: QR code-based invitations with attendee tracking

### Nigerian Market Focus
- **Local Payment Methods**: Integration with Paystack and Flutterwave for Naira transactions
- **Student Verification**: Special discounts and verification for students
- **Offline Capability**: Works in areas with limited internet connectivity
- **Street Party Support**: Features tailored for community gatherings

### Technical Features
- **Progressive Web App (PWA)**: Installable on mobile devices with offline functionality
- **Responsive Design**: Fully responsive for all device sizes
- **SEO Optimization**: Meta tags, structured data, and sitemaps for search engine visibility
- **Security**: Secure authentication and payment processing

### Monetization
- **Ticket Sales Commission**: Earn revenue from ticket sales
- **Invitation Fees**: Charge for premium invitation features
- **Premium Features**: Subscription model for advanced event management tools
- **Sponsored Listings**: Paid placement for featured events

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database management
- **SQLite**: Default database (PostgreSQL support for production)
- **Flask-Login**: User authentication
- **Flask-WTF**: Form handling and validation

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Bootstrap Icons**: Icon library
- **Vanilla JavaScript**: Client-side interactivity
- **Service Workers**: Offline functionality and caching

### Payment Processing
- **Paystack**: Nigerian payment gateway integration
- **Flutterwave**: Alternative payment processor

### SEO & Marketing
- **Structured Data**: Schema.org markup for events
- **Sitemap Generation**: Dynamic XML sitemaps
- **Meta Tags**: Open Graph and Twitter Card support
- **Blog System**: Content marketing platform

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/partyticket-nigeria.git
   cd partyticket-nigeria
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .flaskenv.example .flaskenv
   # Edit .flaskenv with your configuration
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   python run.py
   ```

### Environment Variables

Create a `.flaskenv` file with the following variables:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PAYSTACK_PUBLIC_KEY=pk_test_your-paystack-public-key
PAYSTACK_SECRET_KEY=sk_test_your-paystack-secret-key
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK-your-flutterwave-public-key
FLUTTERWAVE_SECRET_KEY=FLWSECK-your-flutterwave-secret-key
```

## Project Structure

```
partyticket-nigeria/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── payment.py
│   │   └── student.py
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       ├── images/
│       └── manifest.json
├── migrations/
├── instance/
├── requirements.txt
├── run.py
├── config.py
└── alembic.ini
```

## Database Models

### User
- Username, email, password
- Student verification status
- Event creation and ticket purchase history

### Event
- Name, description, date, location
- Ticket price and category
- Organizer relationship

### Ticket
- Event and user relationships
- Payment status and QR code
- Scan verification tracking

### Invitation
- Event relationship
- Max attendees and QR code
- Attendee count tracking

### BlogPost
- Title, excerpt, and content
- Author and publication date
- Category and SEO metadata

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Events
- `GET /events` - List all events
- `GET /events/category/<category>` - Events by category
- `GET /event/<event_id>` - Event details
- `POST /create_event` - Create new event (authenticated)

### Tickets and Invitations
- `POST /create_invitation` - Create invitation (authenticated)
- `GET /invitation/<invitation_id>` - Invitation details (authenticated)
- `POST /api/verify_ticket` - Ticket verification

### SEO
- `GET /robots.txt` - Robots.txt file
- `GET /sitemap.xml` - Dynamic sitemap

## SEO Features

### Meta Tags
- Dynamic page titles and descriptions
- Open Graph tags for social sharing
- Twitter Card meta tags
- Canonical URLs

### Structured Data
- Organization schema for homepage
- Event schema for event pages
- Blog post schema for articles

### Performance
- Minified CSS and JavaScript
- Lazy loading for images
- Service worker for offline functionality
- Asynchronous loading of external scripts

## Content Marketing

### Blog System
The platform includes a built-in blog with:
- Event planning guides
- Cultural celebration articles
- Music and entertainment content
- Campus life resources
- Business and networking advice

### SEO Content Strategy
- Keyword research and optimization
- Regular content updates
- Internal linking structure
- Social media integration

## Monetization Strategies

### Revenue Streams
1. **Commission Model**: Take a percentage of each ticket sale
2. **Premium Features**: Subscription-based advanced tools
3. **Sponsored Listings**: Paid placement in event listings
4. **Advertisement Space**: Banner ads for relevant businesses
5. **Affiliate Partnerships**: Earn commissions from partner services

### Pricing Structure
- **Basic Plan**: Free for event organizers with standard features
- **Premium Plan**: ₦5,000/month for advanced features and priority support
- **Enterprise Plan**: Custom pricing for large organizations

### Payment Processing Fees
- Standard ticket sales: 3.5% + ₦50 per transaction
- Premium subscriptions: 5% processing fee
- Sponsored listings: Fixed monthly rates

## Deployment

The application can be deployed to any platform that supports Python:
- **Heroku**: Simple deployment with add-on databases
- **AWS Elastic Beanstalk**: Scalable cloud deployment
- **Google Cloud Platform**: Flexible hosting options
- **DigitalOcean App Platform**: Cost-effective solution
- **Self-hosted**: Deploy on your own servers

## Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **CSRF Protection**: Enabled via Flask-WTF
- **SQL Injection Prevention**: Uses SQLAlchemy ORM
- **XSS Protection**: Security headers configured
- **Secure Headers**: X-Content-Type-Options, X-Frame-Options, etc.
- **Input Validation**: Form validation on all user inputs

## Error Handling

The application includes comprehensive error handling:
- Custom 404, 403, and 500 error pages
- Database transaction rollback on errors
- Logging for debugging and monitoring
- User-friendly error messages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Heroku
- Railway
- DigitalOcean
- AWS Elastic Beanstalk
- Self-hosted VPS

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on the GitHub repository or contact the development team.

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Event creation and management
- Ticket sales system
- QR code invitations
- Payment integration (Paystack & Flutterwave)
- Student verification
- Blog system
- SEO optimization
- PWA support
- Offline functionality

---

*PartyTicket Nigeria - Connecting People Through Events*