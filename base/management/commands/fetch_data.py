import asyncio
from django.core.management.base import BaseCommand
from base.context_processors import update_local_data  # Adjust import path

class Command(BaseCommand):
    help = "Fetch latest menu data and store locally"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching latest menu data...")
        asyncio.run(update_local_data())
        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))