import random
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Генерация фиктивных данных для пользователей'

    def handle(self, *args, **kwargs):
        self.stdout.write("Генерация пользователей...")

        # Генерация пользователей
        for _ in range(10):  # Генерируем 10 пользователей
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",  # Вы можете использовать другой пароль
                role=random.choice(['COMPANY', 'APPLICANT']),
                company_name=fake.company() if random.choice([True, False]) else '',
                phone_number=fake.phone_number()[:13],
            )
            user.save()

        self.stdout.write("10 пользователей успешно сгенерированы.")
