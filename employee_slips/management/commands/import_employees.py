# employee_slips/management/commands/import_employees.py

import csv
from django.core.management.base import BaseCommand
from employee_slips.models import Employee
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Import employees from a CSV file'

    def add_arguments(self, parser):
        # ตั้งชื่อไฟล์ CSV ที่จะอ่าน
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        # ตรวจสอบว่าพนักงานมีอยู่แล้วหรือไม่ ถ้ายังไม่มีเลยถึงจะ import
        if Employee.objects.exists():
            self.stdout.write(self.style.WARNING('Employees already exist. Skipping import.'))
            return

        self.stdout.write("Starting employee import...")
        
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                employees_to_create = []
                for row in reader:
                    # สร้าง Employee object แต่ยังไม่บันทึกลง DB
                    employee = Employee(
                        employee_id=row['employee_id'].upper(),
                        password=make_password(row['password']), # เข้ารหัสรหัสผ่าน
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                    employees_to_create.append(employee)
                
                # ใช้ bulk_create เพื่อเพิ่มข้อมูลทั้งหมดในครั้งเดียว (เร็วกว่ามาก)
                Employee.objects.bulk_create(employees_to_create)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(employees_to_create)} employees.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found at: {csv_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))