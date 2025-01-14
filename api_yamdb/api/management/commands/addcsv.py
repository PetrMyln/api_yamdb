import csv
import sqlite3

from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,

)
from users.models import MyUser

CSV_DATA = {
    MyUser: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',

}

FILE_WITH_TITLES_GENRE = 'static\\data\\genre_title.csv'


class Command(BaseCommand):
    help = 'Add csv files from static/data/ dir in data base'

    def handle(self, *args, **kwargs):
        for model, file_name in CSV_DATA.items():
            file_name = 'static\\data' + '\\' + file_name
            with open(file_name, encoding='utf-8') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    try:
                        model.objects.create(**row).save()
                    except Exception:
                        pass
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        data_for_db = list()
        with open(FILE_WITH_TITLES_GENRE, encoding='utf-8') as file:
            data = file.readlines()
            for c in data:
                data_for_db.append(c[:-1].split(','))
        cur.execute(''' 
        CREATE TABLE IF NOT EXISTS genre_title ( 
        id INTEGER PRIMARY KEY, 
        title_id TEXT  NOT NULL, 
        genre_id TEXT  NOT NULL 
        ); 
        ''')
        con.commit()
        cur.executemany(
            'INSERT INTO genre_title VALUES(?, ?, ?)',
            data_for_db[1:])
        con.commit()
        con.close()


