# employee_slips/management/commands/create_employee.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from employee_slips.models import Employee

class Command(BaseCommand):
    help = 'Create a new employee with a hashed password'

    def add_arguments(self, parser):
        parser.add_argument('employee_id', type=str, help='The employee ID')
        parser.add_argument('password', type=str, help='The employee password (4 digits)')

    def handle(self, *args, **kwargs):
        employee_id = kwargs['employee_id'].upper()
        password = kwargs['password']

        # เข้ารหัสรหัสผ่าน
        hashed_password = make_password(password)

        # สร้างหรืออัปเดตพนักงาน
        employee, created = Employee.objects.update_or_create(
            employee_id=employee_id,
            defaults={'password': hashed_password}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created employee "{employee_id}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated password for employee "{employee_id}"'))


