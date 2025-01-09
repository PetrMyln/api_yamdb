from django.core.management.base import BaseCommand

import csv

from reviews.models import (
    Comment,
    Review,
    Categories,
    Titles,
    Genre
)

from users.models import MyUser

csv_data = {
    MyUser: 'users.csv',
    Genre: 'genre.csv',
    Categories: 'category.csv',
    Titles: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',

}


class Command(BaseCommand):
    help = 'Add csv files from static/data/ dir in data base'

    def handle(self, *args, **kwargs):
        for model, file_name in csv_data.items():
            file_name = 'static\data' + '\\' + file_name
            with open(file_name, encoding='utf-8') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    try:
                        a = model.objects.create(**row)
                    except Exception as e:
                        pass
