import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    """
    Класс для импорта данных из csv файлов в базу данных.
    """

    def handle(self, *args, **options):

        self.load_data()

    def load_data(self):
        """
        Считывает данные из csv файлов и сохраняет их в базу данных.
        """
        root_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))))
        data_dir = os.path.join(root_dir, 'static', 'data')

        models = {
            'users.csv': User,
            'category.csv': Category,
            'genre.csv': Genre,
            'titles.csv': Title,
            'genre_title.csv': (Genre, Title),
            'review.csv': Review,
            'comments.csv': Comment,
        }

        for filename, model in models.items():
            file_path = os.path.join(data_dir, filename)

            with open(file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        if model == Title:
                            category = Category.objects.get(id=row['category'])
                            row['category'] = category
                        elif model in (Review, Comment):
                            author = User.objects.get(id=row['author'])
                            row['author'] = author
                        if isinstance(model, tuple):
                            genre = Genre.objects.get(id=row['genre_id'])
                            title = Title.objects.get(id=row['title_id'])
                            title.genre.add(genre)
                        else:
                            instance = model(**row)
                            instance.save()
                    except Exception as error:
                        self.stdout.write(
                            self.style.ERROR(
                                'Error while importing data: %s' % error
                            )
                        )
                        continue
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported data from %s' % filename)
            )
        self.stdout.write(
            self.style.SUCCESS('Imported all data')
        )
