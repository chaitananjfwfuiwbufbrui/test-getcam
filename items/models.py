from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
# Create your modfels here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE )
    photo = models.ImageField(upload_to = 'users/%y/%m/%d',blank = True)

    id_proof = models.ImageField(upload_to = 'users/%id/%y/%m/%d',blank = True)
    profile_verified = models.BooleanField(default=False)

    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    phone_verified = models.BooleanField(default=False)

    otp = models.IntegerField(max_length=6,default=000000)

    def __str__(self):
        return f"profile for user {self.user.username}"