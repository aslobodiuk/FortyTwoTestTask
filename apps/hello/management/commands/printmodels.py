from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_models = models.get_models()
        for model in all_models:
            string = '%s have %s object'
            n = model.objects.all().count()
            if n != 1:
                string += "s"
            self.stderr.write(("error: " + string) % (model.__name__, n))
            self.stdout.write(string % (model.__name__, n))
