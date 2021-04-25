import importlib
import inspect
import json

from django.apps import AppConfig
from open_data.settings import CUSTOM_APPS, BADGES_PATH


def is_abstract(cls):
    try:
        return bool(cls.__abstractmethods__)
    except AttributeError:
        return False


class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.base import Badge

        # This function needs to be define here because it requires to import the Badge class
        # which requires the app to be loaded before being imported.
        # Else it would throw an AppRegistryNotReady exception.
        def is_badge(cls):
            """Check recursively if the class is a suptype of Badge."""
            if Badge in cls.__bases__:
                return True
            if object in cls.__bases__:
                return False

            for base_cls in cls.__bases__:
                if is_badge(base_cls):
                    return True
            return False

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
                classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass)
                           if is_badge(cls) and not is_abstract(cls)]
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
