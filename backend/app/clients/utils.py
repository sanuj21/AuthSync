from django.conf import settings
from .models import ClientApp

def load_settings_from_db(client_app_id):
    client_app = ClientApp.objects.get(id=client_app_id)
    setattr(settings, 'CLIENT_APP_SETTINGS', client_app.settings)
