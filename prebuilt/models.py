from django.db import models

class PrebuiltStore(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField("Store Image")
    store_link = models.URLField("Store Link")
    password = models.CharField(max_length=100, blank=True)  # optional

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
