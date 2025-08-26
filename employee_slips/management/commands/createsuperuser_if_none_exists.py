# employee_slips/management/commands/createsuperuser_if_none_exists.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# เราจะใช้ User Model มาตรฐานของ Django สำหรับ Superuser
User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exist'

    def handle(self, *args, **kwargs):
        # ตรวจสอบว่ามี User อยู่ในระบบแล้วหรือยัง
        if User.objects.exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists. Skipping.'))
            return

        # ดึงข้อมูลจาก Environment Variables ที่เราตั้งไว้ใน Render
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables: DJANGO_SUPERUSER_USERNAME, '
                'DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD'
            ))
            return

        self.stdout.write('Creating superuser...')
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))