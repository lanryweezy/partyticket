from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, make_response, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Event, Ticket, Invitation, BlogPost, User
from app.email_utils import send_ticket_confirmation_email
from app.forms import EventForm, TicketForm, InvitationForm, BlogPostForm
import qrcode
import base64
from io import BytesIO
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Homepage route."""
    # Get featured events
    featured_events = Event.query.order_by(Event.date.desc()).limit(6).all()
    return render_template('index.html', featured_events=featured_events)

@main.route('/events')
def events():
    """Events listing route."""
    # Group events by category
    categories = ['formal', 'campus', 'street', 'concert', 'festival', 'general']
    events_by_category = {}
    
    for category in categories:
        events_by_category[category] = Event.query.filter_by(category=category).order_by(Event.date.desc()).limit(3).all()
    
    return render_template('events.html', events_by_category=events_by_category)

@main.route('/events/category/<category>')
def events_by_category(category):
    """Events by category route."""
    valid_categories = ['formal', 'campus', 'street', 'concert', 'festival', 'general']
    if category not in valid_categories:
        flash('Invalid category', 'danger')
        return redirect(url_for('main.events'))
    
    category_events = Event.query.filter_by(category=category).order_by(Event.date.desc()).all()
    return render_template('category_events.html', events=category_events, category=category)

@main.route('/search')
def search_events():
    """Event search route."""
    query = request.args.get('q')
    category = request.args.get('category', 'all')
    
    if query:
        if category != 'all':
            events = Event.query.filter(
                db.and_(
                    Event.category == category,
                    db.or_(
                        Event.name.contains(query),
                        Event.description.contains(query),
                        Event.location.contains(query)
                    )
                )
            ).order_by(Event.date.desc()).all()
        else:
            events = Event.query.filter(
                db.or_(
                    Event.name.contains(query),
                    Event.description.contains(query),
                    Event.location.contains(query)
                )
            ).order_by(Event.date.desc()).all()
    else:
        if category != 'all':
            events = Event.query.filter_by(category=category).order_by(Event.date.desc()).all()
        else:
            events = Event.query.order_by(Event.date.desc()).all()
            
    return render_template('search_results.html', events=events, query=query, category=category)

@main.route('/event/<int:event_id>')
def event_detail(event_id):
    """Event detail route."""
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@main.route('/event/<int:event_id>/buy-tickets', methods=['GET', 'POST'])
@login_required
def buy_tickets(event_id):
    """Ticket purchase route."""
    event = Event.query.get_or_404(event_id)
    form = TicketForm()
    
    if form.validate_on_submit():
        quantity = form.quantity.data
        total_amount = event.price * quantity
        
        try:
            # Create tickets
            tickets = []
            for _ in range(quantity):
                ticket = Ticket(
                    event_id=event.id,
                    user_id=current_user.id,
                    amount_paid=event.price
                )
                db.session.add(ticket)
                tickets.append(ticket)
            
            # Update organizer earnings (platform fee is visual only for now)
            organizer = User.query.get(event.organizer_id)
            if organizer:
                organizer.earnings += total_amount
            
            db.session.commit()

            # Send confirmation email with QR codes
            send_ticket_confirmation_email(current_user, event, tickets)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while processing your purchase. Please try again.', 'danger')
            current_app.logger.error(f'Error purchasing tickets: {str(e)}')
            return render_template('buy_tickets.html', event=event, form=form)
        
        flash(f'Successfully purchased {quantity} ticket(s) for {event.name}! A confirmation email has been sent to {current_user.email}.', 'success')
        return redirect(url_for('main.event_detail', event_id=event.id))
    
    return render_template('buy_tickets.html', event=event, form=form)

@main.route('/invitation/<int:invitation_id>')
@login_required
def invitation_detail(invitation_id):
    """Invitation detail route."""
    invitation = Invitation.query.get_or_404(invitation_id)
    event = Event.query.get_or_404(invitation.event_id)
    return render_template('invitation_detail.html', invitation=invitation, event=event)

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route."""
    # Get user's events by category
    user_events = Event.query.filter_by(organizer_id=current_user.id).all()
    events_by_category = {}
    for event in user_events:
        if event.category not in events_by_category:
            events_by_category[event.category] = []
        events_by_category[event.category].append(event)
    
    # Get user's tickets and invitations
    user_tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    user_invitations = Invitation.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                         events_by_category=events_by_category,
                         tickets=user_tickets,
                         invitations=user_invitations)

@main.route('/admin-dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard route."""
    # Statistics
    total_events = Event.query.count()
    total_tickets = Ticket.query.count()
    total_invitations = Invitation.query.count()
    total_users = User.query.count()
    
    # Recent events
    recent_events = Event.query.order_by(Event.date.desc()).limit(5).all()
    
    # Recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.id.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_events=total_events,
                         total_tickets=total_tickets,
                         total_invitations=total_invitations,
                         total_users=total_users,
                         recent_events=recent_events,
                         recent_tickets=recent_tickets)

@main.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Event creation route."""
    form = EventForm()
    if form.validate_on_submit():
        try:
            # Validate date is in the future
            if form.date.data < datetime.utcnow():
                flash('Event date must be in the future.', 'danger')
                return render_template('create_event.html', form=form)
            
            event = Event(
                name=form.name.data, 
                description=form.description.data, 
                date=form.date.data, 
                location=form.location.data, 
                price=form.price.data, 
                invitation_fee=form.invitation_fee.data,
                category=form.category.data,
                organizer_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating event: {str(e)}')
            flash('An error occurred while creating the event. Please try again.', 'danger')
    return render_template('create_event.html', form=form)

@main.route('/create_invitation', methods=['GET', 'POST'])
@login_required
def create_invitation():
    """Invitation creation route."""
    form = InvitationForm()
    if form.validate_on_submit():
        try:
            # Check if event exists and belongs to current user
            event = Event.query.filter_by(id=form.event_id.data, organizer_id=current_user.id).first()
            if not event:
                flash('Invalid event ID or you do not own this event.', 'danger')
                return render_template('create_invitation.html', form=form)
                
            # Calculate cost
            invitation_cost = event.invitation_fee * form.max_attendees.data
            
            invitation = Invitation(
                event_id=form.event_id.data, 
                user_id=current_user.id, 
                max_attendees=form.max_attendees.data,
                amount_paid=invitation_cost
            )
            db.session.add(invitation)
            db.session.flush()  # Get the invitation ID

            # Generate QR code
            qr_data = f"invitation_id:{invitation.id}"
            qr_img = qrcode.make(qr_data)
            buffered = BytesIO()
            qr_img.save(buffered, format="PNG")
            qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            invitation.qr_code = qr_code_base64
            
            # Update organizer earnings
            organizer = User.query.get(event.organizer_id)
            if organizer:
                organizer.earnings += invitation_cost
                
            db.session.commit()

            flash('Invitation created successfully!', 'success')
            return redirect(url_for('main.invitation_detail', invitation_id=invitation.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating invitation: {str(e)}')
            flash('An error occurred while creating the invitation. Please try again.', 'danger')
    return render_template('create_invitation.html', form=form)

@main.route('/blog')
def blog():
    """Blog listing route."""
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

@main.route('/blog/post/<slug>')
def blog_post(slug):
    """Blog post detail route."""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('blog_post.html', post=post)

@main.route('/admin/blog')
@login_required
def admin_blog():
    """Admin blog management route."""
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin_blog.html', posts=posts)

@main.route('/admin/blog/create', methods=['GET', 'POST'])
@login_required
def create_blog_post():
    """Blog post creation route."""
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            slug=form.slug.data,
            published=form.published.data,
            author_id=current_user.id,
            date_posted=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('main.admin_blog'))
    return render_template('create_blog_post.html', form=form)

@main.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    """Blog post editing route."""
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.excerpt = form.excerpt.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.published = form.published.data
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('main.admin_blog'))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.excerpt.data = post.excerpt
        form.content.data = post.content
        form.slug.data = post.slug
        form.published.data = post.published
    
    return render_template('edit_blog_post.html', form=form, post=post)

# API endpoint for offline ticket verification
@main.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    """User profile route."""
    user = User.query.get_or_404(user_id)
    # Only allow users to view their own profile
    if user.id != current_user.id:
        flash('You can only view your own profile.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user_events = Event.query.filter_by(organizer_id=user.id).count()
    user_tickets = Ticket.query.filter_by(user_id=user.id).count()
    
    return render_template('profile.html', 
                         user=user, 
                         events_count=user_events,
                         tickets_count=user_tickets)

@main.route('/offline-verification')
@login_required
def offline_verification():
    """Offline ticket verification page."""
    return render_template('offline_verification.html')

@main.route('/api/verify_ticket', methods=['POST'])
def verify_ticket():
    """API endpoint for ticket verification."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request data'}), 400
            
        invitation_id = data.get('invitation_id')
        
        if not invitation_id:
            return jsonify({'success': False, 'message': 'Missing invitation ID'}), 400
        
        invitation = Invitation.query.get(invitation_id)
        if not invitation:
            return jsonify({'success': False, 'message': 'Invalid invitation'}), 404
        
        # Check if attendee limit has been reached
        if invitation.attendee_count >= invitation.max_attendees:
            return jsonify({'success': False, 'message': 'Attendee limit reached'}), 400
        
        # Increment attendee count
        invitation.attendee_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Ticket verified successfully',
            'attendee_count': invitation.attendee_count,
            'max_attendees': invitation.max_attendees
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred during verification'}), 500

# SEO routes with enhanced functionality
@main.route('/robots.txt')
def robots_txt():
    """Enhanced robots.txt route."""
    response = make_response('''User-agent: *
Disallow: /admin/
Disallow: /login
Disallow: /register
Disallow: /profile/
Disallow: /dashboard/
Disallow: /create_event
Disallow: /create_invitation
Disallow: /offline-verification
Disallow: /student-verification
Disallow: /api/

Sitemap: https://partyticket.ng/sitemap.xml

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: *
Disallow: /*?
Allow: /events$
Allow: /events/
Allow: /blog$
Allow: /blog/

# Media
Allow: /static/images/
Allow: /static/css/
Allow: /static/js/

# Prevent indexing of certain files
Disallow: /*.pdf$
Disallow: /*.doc$
Disallow: /*.xls$
Disallow: /*.ppt$

# Rate limiting
Crawl-delay: 1''')
    response.headers['Content-Type'] = 'text/plain'
    return response

@main.route('/sitemap.xml')
def sitemap_xml():
    """Dynamic sitemap.xml route with all content."""
    # Create the root element
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    # Add static URLs
    static_urls = [
        ('/', '2023-06-01', 'daily', '1.0'),
        ('/events', '2023-06-01', 'hourly', '0.9'),
        ('/events/category/formal', '2023-06-01', 'hourly', '0.8'),
        ('/events/category/campus', '2023-06-01', 'hourly', '0.8'),
        ('/events/category/street', '2023-06-01', 'hourly', '0.8'),
        ('/events/category/concert', '2023-06-01', 'hourly', '0.8'),
        ('/events/category/festival', '2023-06-01', 'hourly', '0.8'),
        ('/register', '2023-06-01', 'monthly', '0.5'),
        ('/login', '2023-06-01', 'monthly', '0.5'),
        ('/blog', '2023-06-01', 'daily', '0.8')
    ]
    
    for url_path, lastmod, changefreq, priority in static_urls:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f'https://partyticket.ng{url_path}'
        lastmod_elem = SubElement(url, 'lastmod')
        lastmod_elem.text = lastmod
        changefreq_elem = SubElement(url, 'changefreq')
        changefreq_elem.text = changefreq
        priority_elem = SubElement(url, 'priority')
        priority_elem.text = priority
    
    # Add dynamic event URLs
    events = Event.query.order_by(Event.date.desc()).limit(1000).all()
    for event in events:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f'https://partyticket.ng/event/{event.id}'
        lastmod_elem = SubElement(url, 'lastmod')
        lastmod_elem.text = event.date.strftime('%Y-%m-%d')
        changefreq_elem = SubElement(url, 'changefreq')
        changefreq_elem.text = 'daily'
        priority_elem = SubElement(url, 'priority')
        priority_elem.text = '0.7'
    
    # Add blog post URLs
    posts = BlogPost.query.filter_by(published=True).all()
    for post in posts:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f'https://partyticket.ng/blog/post/{post.slug}'
        lastmod_elem = SubElement(url, 'lastmod')
        lastmod_elem.text = post.date_posted.strftime('%Y-%m-%d')
        changefreq_elem = SubElement(url, 'changefreq')
        changefreq_elem.text = 'monthly'
        priority_elem = SubElement(url, 'priority')
        priority_elem.text = '0.6'
    
    # Convert to string
    rough_string = tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Remove empty lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)
    
    response = make_response(pretty_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response