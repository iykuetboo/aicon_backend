from django.db import models

# Create your models here.
class GeneratedImage(models.Model):
    request_id = models.IntegerField(default=None)
    img_idx = models.IntegerField(default=None)
    img_url = models.CharField(max_length=1000, default=None)
    image = models.ImageField(upload_to='img/', default=None)
    # img_bytes = models.BinaryField(default=None)
    def __str__(self):
        return str(self.request_id)

