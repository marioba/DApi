from django.db import models


class Data(models.Model):
    customer_id = models.IntegerField(null=False)
    dialog_id = models.IntegerField(null=False)
    text = models.TextField(null=False, blank=False)
    language = models.CharField(max_length=2, blank=False, null=False)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
