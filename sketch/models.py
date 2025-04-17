from django.db import models

class SketchImage(models.Model):
    original = models.ImageField(upload_to="uploads/")
    sketch = models.ImageField(upload_to="sketches/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sketch {self.id}"
