from django.shortcuts import render

from badge.models import BadgeAward
from badge.registry import BadgeCache


def badge_list(request):
    user = request.user
    cache = BadgeCache.instance()

    # Make a list of every available badge
    badges = {}
    for badge in cache._registry.values():  # TODO: make this a public field (or available at least)
        for level in range(len(badge.levels)):
            name = f'{badge.slug}:{level}'
            badges[name] = {
                'slug': badge.slug,
                'level': level,
                'name': badge.levels[level].name,
                'description': badge.levels[level].description,
                'image': badge.levels[level].image,
                'x': badge.positions[level][0],
                'y': badge.positions[level][1],
                'visible': False,
                'earned': False,
            }
            
    # Annotate earned badges
    visible_positions = set()
    if user.is_authenticated:
        for badge_obj in user.badges_earned.all():
            name = f'{badge_obj.slug}:{badge_obj.level}'
            badge = badges[name]

            badge['earned'] = True

            x, y = badge['x'], badge['y']
            visible_positions.add((x, y))
            visible_positions.add((x, y - 1))
            visible_positions.add((x + 1, y))
            visible_positions.add((x, y + 1))
            visible_positions.add((x - 1, y))

    # Annotate visible badges
    for badge in badges.values():
        if (badge['x'], badge['y']) in visible_positions:
            badge['visible'] = True

    print(badges)
    return render(request, 'badges.html', {'badges': badges})


def badge_detail(request, slug, level):
    badge = BadgeCache.instance().get_badge(slug).levels[int(level)]
    badge_awards = BadgeAward.objects.filter(
        slug=slug,
        level=level
    ).order_by("-awarded_at")

    badge_count = badge_awards.count()
    latest_awards = badge_awards[:50]

    return render(request, "badge_detail.html", {
        "badge": badge,
        "badge_count": badge_count,
        "latest_awards": latest_awards,
    })
