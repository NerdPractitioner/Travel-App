from django.apps import AppConfig


class UserprofilesConfig(AppConfig):
    name = 'UserProfiles'

    def ready(self):
        import UserProfiles.signals
