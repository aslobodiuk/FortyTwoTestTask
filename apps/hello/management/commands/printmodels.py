from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_models = models.get_models()
        for model in all_models:
            n = model.objects.all().count()
            string = '%s have %s object' % (model.__name__, n)
            if n != 1:
                string += "s"
            self.stderr.write("error: " + string)
            self.stdout.write(string)
