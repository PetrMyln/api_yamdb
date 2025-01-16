import sqlite3
from csv import DictReader

from django.core.management.base import BaseCommand

from api_yamdb.constant import FILE_GENRE_TITLE, STATIC_DIR_FOR_CSV_FILES
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)

from users.models import User

CSV_DATA = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Add csv files from static/data/ dir in data base'

    def handle(self, *args, **kwargs):
        for model, file_name in CSV_DATA.items():
            file_name = STATIC_DIR_FOR_CSV_FILES + file_name
            with open(file_name, encoding='utf-8') as file:
                rows = DictReader(file)
                for row in rows:
                    try:
                        model.objects.create(**row).save()
                    except Exception:
                        pass
        data_for_db = list()
        with open(FILE_GENRE_TITLE, encoding='utf-8') as file:
            data = file.readlines()
            for c in data:
                data_for_db.append(c[:-1].split(','))
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        cur.executemany(
            'INSERT INTO reviews_title_genre VALUES(?, ?, ?)',
            data_for_db[1:])
        con.commit()
        con.close()
