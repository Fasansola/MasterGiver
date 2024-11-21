# In your Django app directory, create or update the file:
# your_app/management/commands/add_giving_styles.py

from django.core.management.base import BaseCommand
from givers.models import GivingStyle  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Adds a set of giving styles to the database'

    def handle(self, *args, **kwargs):
        giving_styles = [
            {
                'name': 'Intentional Giver',
                'description': "I'm organized and committed in my giving. I plan my donations ahead, knowing exactly who, how much, and when I'll give each month or year."
            },
            {
                'name': 'Spontaneous Giver',
                'description': "I give whenever something resonates with me. No set plans or tracking—if I feel moved to support a cause, I just go for it."
            },
            {
                'name': 'Impact-Driven Giver',
                'description': "I focus on making a measurable difference. My time and money go only to causes with clear, quantifiable results. I believe in purposeful impact over what is popular."
            },
            {
                'name': 'Giver of Time',
                'description': "I donate my time and skills rather than money. For me, volunteering is the most meaningful way to give back to the causes I care about."
            },
            {
                'name': 'The 10% Giver',
                'description': "Giving 10% of my income is my way of staying connected to my values. This consistent approach—through my church or chosen causes—is my main way of giving back."
            },
            {
                'name': 'Heartfelt Giver',
                'description': "I give when a cause touches my heart. When something deeply moves me, I can't help but lend my support however I can."
            }
        ]

        for style_data in giving_styles:
            style, created = GivingStyle.objects.get_or_create(
                name=style_data['name'],
                defaults={'description': style_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added giving style: {style_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Giving style already exists: {style_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'Finished adding {len(giving_styles)} giving styles'))