# employee_slips/models.py
from django.db import models
from django.contrib.auth.hashers import make_password
from cloudinary.models import CloudinaryField

class Employee(models.Model):
    # รหัสพนักงาน, ทำให้เป็น Primary Key เพื่อไม่ให้ซ้ำกัน
    employee_id = models.CharField(max_length=20, primary_key=True) 
    
    # รหัสผ่าน (เราจะเก็บรหัสที่เข้ารหัสแล้ว ไม่ใช่เลข 4 ตัวตรงๆ)
    password = models.CharField(max_length=128) 

    # เพิ่ม field อื่นๆ ได้ในอนาคต เช่น ชื่อ, นามสกุล
    first_name = models.CharField(max_length=100, blank=True) # blank=True คือไม่จำเป็นต้องกรอก
    last_name = models.CharField(max_length=100, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.employee_id

# --- เพิ่ม Model ใหม่นี้เข้าไป ---
class Slip(models.Model):
    # เชื่อมโยงไปยังพนักงานที่เป็นเจ้าของสลิป
    # on_delete=models.CASCADE หมายความว่าถ้าพนักงานถูกลบ สลิปของเขาก็จะถูกลบไปด้วย
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='slips')

    # เดือนและปีของสลิป
    month = models.IntegerField() # เก็บเป็นตัวเลข 1-12
    year = models.IntegerField() # เก็บเป็นตัวเลข ค.ศ. เช่น 2024

    # ที่อยู่ของไฟล์รูปภาพบน Cloudinary
    # เราจะใช้ CharField ไปก่อน แล้วค่อยเปลี่ยนเป็น CloudinaryField ทีหลัง
    image = CloudinaryField('image', null=True, blank=True)

    # วันที่อัปโหลด (ให้ระบบใส่ให้เองอัตโนมัติ)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slip for {self.employee.employee_id} - {self.month}/{self.year}"

    class Meta:
        # ทำให้สลิปของพนักงานคนหนึ่ง ในเดือนและปีเดียวกัน มีได้แค่ใบเดียว
        unique_together = ('employee', 'month', 'year')
