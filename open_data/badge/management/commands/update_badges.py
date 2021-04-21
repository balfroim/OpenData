import json

from django.core.management.base import BaseCommand

from ...registry import BadgeCache
from open_data.settings import BADGES_PATH


class Command(BaseCommand):
    help = 'Update the badge list with newly added badges.'

    def handle(self, *args, **options):
        badge_cache = BadgeCache.instance()._registry  # TODO: this is a hack, fix it (later)
        try:
            with open(BADGES_PATH, 'r') as file:
                badges = json.load(file)
        except FileNotFoundError:
            badges = {}

        added_badges = set()
        current_badges = set()
        for badge in badge_cache.values():
            for level in range(len(badge.levels)):
                name = f'{badge.slug}:{level}'
                name_deleted = f'deleted:{name}'
                current_badges.add(name)
                if name not in badges:
                    added_badges.add(name)
                    if name_deleted in badges:
                        badges[name] = badges[name_deleted]
                        del badges[name_deleted]
                        self.stdout.write(f'{name!r} badge undeleted.')
                    else:
                        badges[name] = {'x': 0, 'y': 0}
                        self.stdout.write(f'{name!r} badge added.')

        deleted_badges = set()
        for name in badges:
            if not name.startswith('deleted:') and name not in current_badges:
                deleted_badges.add(name)
                self.stdout.write(f'{name!r} badge removed.')

        for name in deleted_badges:
            deleted_name = f'deleted:{name}'
            badges[deleted_name] = badges[name]
            del badges[name]

        with open(BADGES_PATH, 'w') as file:
            json.dump(badges, file, indent='  ')

        n_badges = len(current_badges) + len(added_badges) - len(deleted_badges)
        self.stdout.write(self.style.SUCCESS(f'{n_badges} badges found: {len(added_badges)} added, {len(deleted_badges)} removed.'))
