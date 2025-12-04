#!/usr/bin/env python
"""
PartyTicket Nigeria - Event Ticketing Platform
Main Application Entry Point
"""

import os
from app import create_app, db
from app.models import User, Event, Ticket, Invitation, BlogPost

# Create the Flask application
app = create_app()

# Register CLI commands
@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Event': Event,
        'Ticket': Ticket,
        'Invitation': Invitation,
        'BlogPost': BlogPost
    }

if __name__ == '__main__':
    # Run the development server
    app.run(
        host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_RUN_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )