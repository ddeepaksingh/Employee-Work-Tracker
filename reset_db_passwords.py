import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Set deepak_singh password
try:
    user = User.objects.get(username="deepak_singh")
    user.set_password("deepakpassword123")
    user.save()
    print("Set deepak_singh password to deepakpassword123")
except User.DoesNotExist:
    print("deepak_singh does not exist")

# Create or set admin_user password
admin_user, created = User.objects.get_or_create(
    username="admin_user",
    defaults={
        "email": "admin@company.com",
        "is_staff": True,
        "is_superuser": True
    }
)
admin_user.set_password("adminpassword123")
admin_user.save()
print("Set admin_user password to adminpassword123")
