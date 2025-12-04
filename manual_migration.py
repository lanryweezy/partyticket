#!/usr/bin/env python
"""
Manual Migration Script for PartyTicket Nigeria
"""

import sys
import os
from app import create_app, db
from app.models import User, Event, Ticket, Invitation, BlogPost

def create_tables():
    """Create all database tables."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("All database tables created successfully!")
        
        print("Migration completed successfully!")

if __name__ == '__main__':
    create_tables()