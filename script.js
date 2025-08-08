// script.js (เวอร์ชันปรับปรุงใหม่)

function login() {
    // 1. สร้างฐานข้อมูลจำลองของพนักงาน
    // Key คือ "รหัสพนักงาน" (ตัวพิมพ์ใหญ่)
    // Value คือ Object ที่มีข้อมูล "วันเกิด"
    const users = {
        "L04424": { birthdate: "20/04/1998" }
        // *** คุณสามารถเพิ่มพนักงานคนต่อไปที่นี่ได้เลย! ***
        // "รหัสพนักงานใหม่": { birthdate: "วว/ดด/ปปปป" },
        // "รหัสพนักงานอีกคน": { birthdate: "วว/ดด/ปปปป" }
    };

    // 2. ดึงค่าจากฟอร์มและจัดรูปแบบ (เหมือนเดิม)
    const employeeIdInput = document.getElementById('employeeId').value.trim();
    const birthdateInput = document.getElementById('birthdate').value.trim();
    const employeeId = employeeIdInput.toUpperCase(); // แปลงเป็นตัวใหญ่เพื่อใช้ค้นหา

    // 3. ค้นหาข้อมูลผู้ใช้ในฐานข้อมูลจำลอง
    const user = users[employeeId]; // ดึงข้อมูลผู้ใช้จากรหัสพนักงาน

    // 4. ตรวจสอบข้อมูล
    // เช็คว่า 1) มีผู้ใช้นี้ในระบบหรือไม่ (user ไม่ใช่ค่าว่าง)
    //        2) วันเกิดที่กรอกมา ตรงกับวันเกิดในระบบหรือไม่
    if (user && user.birthdate === birthdateInput) {
        // ถ้าทุกอย่างถูกต้อง
        window.open(`payslip.html?employeeId=${employeeId}`, "_self");
    } else {
        // ถ้าข้อมูลไม่ถูกต้อง
        alert("รหัสพนักงานหรือวัน/เดือน/ปีเกิดไม่ถูกต้อง\nกรุณาตรวจสอบข้อมูลอีกครั้ง");
    }

    return false;
}