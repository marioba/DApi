from django.db import models


class Dialog(models.Model):
    """This class represent a customer input during their dialog with the chatbot."""

    dialog_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField(null=False)
    text = models.TextField(null=False, blank=False)
    language = models.CharField(max_length=2, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Consent(models.Model):
    """This class represent the approval of the customer to use their dialog data. It has a
    one to one relation with a Dialog"""

    dialog = models.OneToOneField(Dialog, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
