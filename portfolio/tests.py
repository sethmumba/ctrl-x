import requests

API_URL = "http://127.0.0.1:8000/portfolio/api/projects/"
HEADERS = {"Content-Type": "application/json"}

image_urls = [
    "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838536/samples/man-on-a-street.jpg",
    "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838537/samples/cup-on-a-table.jpg",
    "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838537/samples/coffee.jpg",
    "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838530/samples/ecommerce/car-interior-design.jpg",
    "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838530/samples/animals/three-dogs.jpg"
]

for i in range(1, 21):
    data = {
        "title": f"Project {i}",
        "description": f"This is the description for project {i}.",
        "image_url": image_urls[i % len(image_urls)],  # rotate through image URLs
        "link": "https://onmart.ae"
    }
    response = requests.post(API_URL, json=data, headers=HEADERS)
    if response.status_code == 201:
        print(f"Project {i} created successfully.")
    else:
        print(f"Failed to create Project {i}: {response.status_code}, {response.text}")
