import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Review, Title
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Add csv files to Django Models.'

    def handle(self, *args, **kwargs):
        try:
            with open(
                'review.csv',
                newline='',
                encoding='utf-8'
            ) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row in spamreader:
                    if (Title.objects.filter(pk=int(row[1]))
                            and CustomUser.objects.filter(pk=int(row[3]))):
                        Review.objects.update_or_create(
                            title_id=Title.objects.get(pk=int(row[1])),
                            text=row[2],
                            author=CustomUser.objects.get(pk=int(row[3])),
                            score=int(row[4]),
                            pub_date=row[5]
                        )
                self.stdout.write(self.style.SUCCESS('Review записан.'))
        except FileNotFoundError:
            raise CommandError("Неудалось открыть файл Review.csv.")
        except Exception:
            raise CommandError("Неудалось записать модель Review.")
