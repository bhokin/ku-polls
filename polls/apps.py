"""The Django config for polls application."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Django polls config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
