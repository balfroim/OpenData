import importlib
import inspect
import json

from django.apps import AppConfig

from open_data.settings import CUSTOM_APPS, BADGES_PATH


class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.base import Badge
        from badge.registry import BadgeCache

        # Get badges' positions from json
        try:
            with open(BADGES_PATH, 'r') as file:
                positions = json.load(file)
        except FileNotFoundError:
            positions = {}

        # Import dynamically all the Badge subclasses in the installed apps.
        for module_name in CUSTOM_APPS:
            try:
                module = importlib.import_module(f"{module_name}.badges", package=None)
            except ModuleNotFoundError:
                pass
            else:
                classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass) if Badge in cls.__bases__]
                for cls in classes:
                    # Retrieve positions from json file
                    # TODO: move this somewhere else...
                    cls.positions = []
                    for i in range(len(cls.levels)):
                        name = f'{cls.slug}:{i}'
                        position = positions.get(name, {'x': 0, 'y': 0})
                        cls.positions.append([position['x'], position['y']])

                    BadgeCache.instance().register(cls)

        badge_awarded = getattr(importlib.import_module("badge.signals"), "badge_awarded")
