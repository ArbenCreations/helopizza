from django.apps import AppConfig
import threading
import asyncio

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        # Avoid running multiple times during migrations or shell
        import sys
        if 'runserver' not in sys.argv and 'gunicorn' not in sys.argv:
            return

        threading.Thread(target=self.run_async_startup, daemon=True).start()

    def run_async_startup(self):
        from . import preload_data_module  # 👈 adjust if file name is different
        asyncio.run(preload_data_module.preload_data())
