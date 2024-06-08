from django.db import models
import uuid

# Create your models here.
class ScrapingJob(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    result = models.JSONField(null=True, blank=True)

