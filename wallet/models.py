from django.db import models
from project.settings import AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    id_hash = models.CharField(max_length = 256)
    qr_code = models.ImageField(upload_to="qrcodes/", height_field=None, width_field=None, max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Wallet for {self.user.username}"