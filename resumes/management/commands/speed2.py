import random
from faker import Faker
from django.core.management.base import BaseCommand
from resumes.models import Resume
from django.contrib.auth import get_user_model
User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Генерация фиктивных данных для резюме'

    def handle(self, *args, **kwargs):
        self.stdout.write("Генерация резюме...")

        # Генерация резюме для всех пользователей
        users = User.objects.all()
        for user in users:
            resume = Resume.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                Birth=fake.date_of_birth(minimum_age=18, maximum_age=65),
                skills=fake.text(max_nb_chars=200),
                gender=random.choice(['M', 'F']),
                city=fake.city(),
                experience=fake.text(max_nb_chars=300),
                education=fake.text(max_nb_chars=200),
                contact_info=fake.text(max_nb_chars=100),
                phone=fake.phone_number()[:13],
            )
            resume.save()

        self.stdout.write("Резюме успешно сгенерированы.")