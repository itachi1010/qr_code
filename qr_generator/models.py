# qr_generator/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class QRCode(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AccessRecord(models.Model):
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True)

# Signal to create an AccessRecord
@receiver(post_save, sender=QRCode)
def create_access_record(sender, instance, **kwargs):
    # Assume instance.url is the URL contained in the QR code
    # This function needs to be called whenever the QR code is accessed, not just saved
    AccessRecord.objects.create(qr_code=instance)
