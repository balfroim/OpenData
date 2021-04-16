import inspect
import importlib
from importlib import import_module
from django.apps import AppConfig
from open_data.settings import INSTALLED_APPS


class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.base import Badge
        from badge.registry import BadgeCache
        for module_name in INSTALLED_APPS:
            try:
                module = importlib.import_module(f"{module_name}.badges", package=None)
            except ModuleNotFoundError:
                pass
            else:
                classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass) if
                           name.endswith("Badge") and name != 'Badge']
                for cls in classes:
                    BadgeCache.instance().register(cls)
        from badge.signals import badge_awarded
