from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Create a simple logo
img = Image.new('RGB', (512, 512), color=(111, 66, 193))  # Purple background
draw = ImageDraw.Draw(img)

# Draw a ticket shape
ticket_points = [(100, 50), (412, 50), (412, 150), (462, 200), (412, 250), (412, 462), (100, 462)]
draw.polygon(ticket_points, fill=(255, 255, 255))

# Draw a perforation line
for i in range(50, 462, 20):
    draw.ellipse([402, i-5, 422, i+5], fill=(111, 66, 193))

# Add text
try:
    # Try to use a better font if available
    font = ImageFont.truetype("arial.ttf", 48)
except:
    # Fallback to default font
    font = ImageFont.load_default()

draw.text((150, 200), "PartyTicket", fill=(111, 66, 193), font=font)
draw.text((180, 260), "Nigeria", fill=(111, 66, 193), font=font)

# Save the logo
img.save('app/static/images/logo.png')

# Also save favicon
favicon = img.resize((32, 32))
favicon.save('app/static/images/favicon.png')

print("Logo and favicon created successfully!")