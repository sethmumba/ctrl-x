from django.core.management.base import BaseCommand
from prebuilt.models import PrebuiltStore
import random

class Command(BaseCommand):
    help = "Create 20 sample prebuilt stores"

    def handle(self, *args, **options):
        image_urls = [
            "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838536/samples/man-on-a-street.jpg",
            "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838537/samples/cup-on-a-table.jpg",
            "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838537/samples/coffee.jpg",
            "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838530/samples/ecommerce/car-interior-design.jpg",
            "https://res.cloudinary.com/djxeu9bfh/image/upload/v1751838530/samples/animals/three-dogs.jpg",
        ]

        PrebuiltStore.objects.all().delete()  # optional: clear old entries

        for i in range(1, 21):
            store = PrebuiltStore.objects.create(
                name=f"Prebuilt Store {i}",
                description=f"This is a description for Prebuilt Store {i}. Fully ready to launch!",
                image_url=random.choice(image_urls),
                store_link="https://onmart.ae",
                password=f"pass{i}123"
            )
            self.stdout.write(self.style.SUCCESS(f"Created store: {store.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully created 20 prebuilt stores!"))
