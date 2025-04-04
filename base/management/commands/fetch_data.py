from django.core.management.base import BaseCommand
from base.context_processors import update_local_data  # Make sure the path is correct

class Command(BaseCommand):
    help = "Fetch latest menu data and store locally"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching latest menu data...")
        update_local_data()  # Just call directly — no asyncio
        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
