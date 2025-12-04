#!/usr/bin/env python
"""
Dynamic Sitemap Generator for PartyTicket Nigeria
Generates XML sitemap for better search engine indexing
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime
from app import create_app, db
from app.models import Event, BlogPost

def generate_sitemap():
    """Generate dynamic sitemap.xml for PartyTicket Nigeria."""
    app = create_app()
    
    with app.app_context():
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
        
        # Write to file
        with open('app/static/sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print("Sitemap generated successfully!")

if __name__ == '__main__':
    generate_sitemap()