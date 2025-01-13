import random
from faker import Faker
from django.core.management.base import BaseCommand
from jobs.models import Job
from django.contrib.auth import get_user_model
User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Генерация фиктивных данных для вакансий'

    def handle(self, *args, **kwargs):
        self.stdout.write("Генерация вакансий...")

        # Генерация вакансий
        users = User.objects.all()  # Предположим, что пользователи уже созданы
        for _ in range(20):  # Генерируем 20 вакансий
            job = Job.objects.create(
                title=fake.job(),
                description=fake.text(max_nb_chars=300),
                location=fake.city(),
                salary=random.randint(50000, 150000),
                currency=random.choice(['USD', 'EUR', 'RUB', 'GBP', 'BYN']),
                company=fake.company(),
                user=random.choice(users),
            )
            job.save()

        self.stdout.write("20 вакансий успешно сгенерированы.")