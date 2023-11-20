from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import choice, randint
from datetime import datetime, timedelta
from faker import Faker
from app.models import Profile, Question, Answer, Tag

fake = Faker()


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Fill ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Create users
        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = []
        for i in range(ratio):
            username = fake.user_name()
            email = fake.email()

            # Check if the user with the same username already exists
            user, created = User.objects.get_or_create(username=username,
                                                       defaults={'email': email, 'password': 'password'})

            # If the user already exists, generate a new username
            while not created:
                username = fake.user_name()
                user, created = User.objects.get_or_create(username=username,
                                                           defaults={'email': email, 'password': 'password'})

            # Create Profile
            profile = Profile.objects.create(user=user, email=email, nickname=username)
            users.append(profile)

        # Create tags
        self.stdout.write(self.style.SUCCESS('Creating tags...'))
        tags = [Tag.objects.create(tag_word=fake.word()) for _ in range(ratio)]

        # Create questions, answers, and user ratings
        self.stdout.write(self.style.SUCCESS('Creating questions, answers, and user ratings...'))
        for i in range(ratio * 10):
            author = choice(users)
            title = fake.sentence()
            content = fake.text()
            question = Question.objects.create(title=title, content=content, author=author,
                                               creation_date=fake.date_between(start_date='-365d', end_date='today'))
            question.tag.set([choice(tags) for _ in range(randint(1, 8))])

            for _ in range(randint(10, 50)):
                answer_author = choice(users)
                answer_content = fake.text()
                is_correct = choice([0, 1])
                answer = Answer.objects.create(content=answer_content, to_question=question, author=answer_author,
                                               is_correct=is_correct,
                                               creation_date=fake.date_between(start_date='-365d', end_date='today'))
                answer.author = answer_author
                question.count()  # Update the answer count in the Question model

                answer.answer_likes += randint(10, 100)
                answer.answer_dislikes += randint(5, 40)
                answer.save()

                question.question_likes += randint(10, 100)
                question.question_dislikes += randint(5, 40)
                question.save()

        self.stdout.write(self.style.SUCCESS('Database filled successfully.'))
