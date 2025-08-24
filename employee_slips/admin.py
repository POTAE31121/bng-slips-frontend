from django import forms
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from .models import Employee, Slip
from django.contrib.auth.hashers import make_password
import os

class EmployeeChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),required=False)

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeChangeForm
    list_display = ('employee_id', 'first_name', 'last_name') #is_staff #is_active
    search_fields = ('employee_id', 'first_name', 'last_name')
    ordering = ('employee_id',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['employee_id']
        else:
            return []

    def save_model(self, request, obj, form, change):
        """
        Override save_model เพื่อเข้ารหัสรหัสผ่านก่อนบันทึก
        """
        # ดึงรหัสผ่านที่ผู้ใช้กรอกมาจากฟอร์มที่ผ่านการตรวจสอบแล้ว
        new_password = form.cleaned_data.get('password')
        
        # --- ส่วนดีบัก ---
        print("--- Inside save_model ---")
        print(f"New password from form: '{new_password}'")
        
        # ถ้ามีรหัสผ่านใหม่ (ผู้ใช้ไม่ได้เว้นว่างไว้)
        if new_password:
            obj.password = make_password(new_password)
            print(f"Hashed password to be saved: {obj.password}")
        else:
            print("Password was not changed. Keeping the old one.")
        
        print("------------------------")

        # บันทึกข้อมูลลงฐานข้อมูล
        super().save_model(request, obj, form, change)

class SlipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'uploaded_at')
    list_filter = ('year', 'month')
    list_display_links = None
    actions = ["export_as_csv"]
    search_fields = ('employee__employee_id', 'employee__first_name', 'employee__last_name')
    ordering = ('-year', '-month', 'employee__employee_id')
    fields = ('employee', 'month', 'year', 'image')
    raw_id_fields = ('employee',)
    change_list_template = "admin/employee_slips/slip/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-multiple-slips/', self.admin_site.admin_view(self.bulk_upload_view), name='employee_slips_bulk_upload_slips'),
        ]
        return custom_urls + urls
    
    def bulk_upload_view(self, request):
        if request.method == 'POST':
            month = request.POST.get('month')
            year = request.POST.get('year')
            slip_files = request.FILES.getlist('slip_files')

            success_count = 0
            error_count = 0

            for slip_file in slip_files:
                try:
                    filename, extension = os.path.splitext(slip_file.name)
                    employee_id = filename.upper()

                    employee = Employee.objects.get(pk=employee_id)

                    Slip.objects.update_or_create(
                        employee=employee,
                        month=month,
                        year=year,
                        defaults={'image': slip_file}
                    )

                    success_count += 1
                except Employee.DoesNotExist:
                    messages.error(request, f"ไม่พบพนักงานที่มีรหัส '{employee_id}' สำหรับไฟล์ '{slip_file.name}'")
                    error_count += 1
                except Exception as e:
                    messages.error(request, f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์ '{slip_file.name}': {str(e)}")
                    error_count += 1
            if success_count > 0:
                messages.success(request, f"อัปโหลดสลิปสำเร็จ {success_count} ไฟล์")
            if error_count == 0 and success_count > 0:
                # ถ้าสำเร็จทั้งหมด ให้กลับไปหน้ารายการสลิป
                return redirect('..')
            # ถ้าเป็นการเปิดหน้าครั้งแรก (GET)
        return render(request, 'admin/employee_slips/slip/bulk_upload_form.html')

    # --- 3. Override changelist_view เพื่อเพิ่มปุ่ม ---
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_button'] = {
            'url': 'upload-multiple-slips/',
            'title': 'Bulk Upload Slips'
        }
        return super().changelist_view(request, extra_context=extra_context)  

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Slip, SlipAdmin)