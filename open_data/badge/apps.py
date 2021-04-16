import importlib
import inspect

from django.apps import AppConfig

from open_data.settings import CUSTOM_APPS


class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.base import Badge
        from badge.registry import BadgeCache
        # Import dynamically all the Badge subclasses in the installed apps.
        for module_name in CUSTOM_APPS:
            try:
                module = importlib.import_module(f"{module_name}.badges", package=None)
            except ModuleNotFoundError:
                pass
            else:
                classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass) if Badge in cls.__bases__]
                for cls in classes:
                    BadgeCache.instance().register(cls)
        badge_awarded = getattr(importlib.import_module("badge.signals"), "badge_awarded")
