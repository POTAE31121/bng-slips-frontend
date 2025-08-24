# employee_slips/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Slip
from django.contrib.auth.hashers import make_password, check_password

# employee_slips/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password # ตรวจสอบว่า import เข้ามาแล้ว
from .models import Employee

def login_page(request):
    error_message = None
    if request.method == 'POST':
        employee_id_input = request.POST.get('employee_id').upper()
        password_input = request.POST.get('password')

        try:
            employee = Employee.objects.get(pk=employee_id_input)
            
            # --- เปลี่ยนจาก '==' มาใช้ check_password ---
            if check_password(password_input, employee.password):
                # ถ้ารหัสผ่านถูกต้อง
                return redirect('slip_display_page', employee_id=employee.employee_id)
            else:
                error_message = "รหัสผ่านไม่ถูกต้อง"
        
        except Employee.DoesNotExist:
            error_message = "ไม่พบรหัสพนักงานนี้ในระบบ"

    context = {'error_message': error_message}
    return render(request, 'employee_slips/login.html', context)

def slip_display_page(request, employee_id):
    # ใช้ get_object_or_404 เพื่อความปลอดภัย
    # ถ้าหาพนักงานไม่เจอ จะขึ้นหน้า 404 แทนที่จะเกิดข้อผิดพลาด
    employee = get_object_or_404(Employee, pk=employee_id)

    # ค้นหา slip ล่าสุดของพนักงานคนนี้
    # กรอง (filter) เฉพาะ slip ของพนักงานนี้)
    # เรียงลำดับ (order_by) จากใหม่ไปเก่า (ปี, เดือน)
    # ดึงมาแค่ใบแรกสุด (lastet)
    lastest_slip = Slip.objects.filter(employee=employee).order_by('-year', '-month').first()

    #employee_id_for_file = employee_id.upper()  # แปลงเป็นตัวพิมพ์ใหญ่เพื่อให้ตรงกับชื่อไฟล์

    context = {
        'employee': employee,
        'slip': lastest_slip, # ส่ง slip ล่าสุดไปที่เทมเพลต
    }
    return render(request, 'employee_slips/slip_display.html', context)