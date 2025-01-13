import random
from faker import Faker
from django.core.management.base import BaseCommand
from resumes.models import Resume
from jobs.models import Job
from user.models import User
from resumes.models import JobApplication

fake = Faker()

class Command(BaseCommand):
    help = 'Генерация фиктивных откликов на вакансии'

    def handle(self, *args, **kwargs):
        self.stdout.write("Генерация откликов...")

        jobs = Job.objects.all()
        resumes = Resume.objects.all()
        for _ in range(50):  # Генерируем 50 откликов
            job = random.choice(jobs)
            resume = random.choice(resumes)
            job_application = JobApplication.objects.create(
                job=job,
                user=resume.user,
                resume=resume,
                cover_letter=fake.text(max_nb_chars=200),
                is_approved=random.choice([True, False]),
                is_read=random.choice([True, False]),
            )
            job_application.save()

        self.stdout.write("50 откликов успешно сгенерированы.")