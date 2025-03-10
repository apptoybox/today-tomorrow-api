from PIL import Image, ImageDraw

# Create a new image with a transparent background
size = (32, 32)
image = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a circle (clock face)
margin = 2
draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], outline=(0, 102, 204), width=2)

# Draw clock hands (pointing to 10:10 for aesthetic reasons)
center = (size[0]//2, size[1]//2)
# Hour hand
draw.line([center, (center[0]-5, center[1]-3)], fill=(0, 102, 204), width=2)
# Minute hand
draw.line([center, (center[0]+7, center[1]-7)], fill=(0, 102, 204), width=2)

# Save the image
image.save('static/favicon.ico', format='ICO')
