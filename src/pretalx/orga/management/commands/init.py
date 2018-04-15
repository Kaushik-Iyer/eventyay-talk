from urllib.parse import urljoin

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.urls import reverse
from django.utils.translation import ugettext as _

from pretalx.event.models import Organiser, Team
from pretalx.person.models import User


class Command(BaseCommand):
    help = 'Initializes your pretalx instance. Only to be used once.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(_('\nWelcome to pretalx! I am the initialization command, and I should be used only once.')))
        self.stdout.write(_('You can abort this command at any time using C-c, and no data will be retained.'))

        self.stdout.write(_('''\nLet\'s get you a user with the right to create new events and access every event on this pretalx instance.'''))

        call_command('createsuperuser')
        user = User.objects.order_by('-id').filter(is_administrator=True).first()

        self.stdout.write(_('''\nLet\'s also create a first organiser: This will allow you to invite further people and create events.'''))

        organiser_name = input(_('\nName (e.g. "The Conference Organiser"): '))
        organiser_slug = input(_('Slug (e.g. "conforg"): '))

        organiser = Organiser.objects.create(name=organiser_name, slug=organiser_slug)
        team = Team.objects.create(
            organiser=organiser, name=f'Team {organiser_name}',
            can_create_events=True, can_change_teams=True,
            can_change_organiser_settings=True,
        )
        team.members.add(user)

        event_url = urljoin(settings.SITE_URL, reverse('orga:event.create'))
        team_url = urljoin(settings.SITE_URL, reverse('orga:organiser.teams.view', kwargs={'organiser': organiser_slug, 'pk': team.pk}))
        self.stdout.write(_('\nNow that this is done, you can:'))
        self.stdout.write(_(' - Create your first event at {event_url}').format(event_url=event_url))
        self.stdout.write(_(' - Invite somebody to the organiser team at {team_url} and let them create the event').format(team_url=team_url))
        self.stdout.write(_(' - Use the command "import_schedule /path/to/schedule.xml" if you want to import an event."'))
