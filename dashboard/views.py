from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from employee.models import Employee
from django.db.models import Sum,Avg
from department.models import Department
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook



def home(request):

    total_employees = Employee.objects.count()

    total_departments = Employee.objects.values(
        "department"
    ).distinct().count()

    total_salary = Employee.objects.aggregate(
        Sum("salary")
    )["salary__sum"] or 0

    average_salary = Employee.objects.aggregate(
        Avg("salary")
    )["salary__avg"] or 0
    department_data = (
        Department.objects.annotate(
            employee_count=Count("employee")
        )
    )

    department_labels = []
    department_counts = []

    for department in department_data:
        department_labels.append(department.name)
        department_counts.append(department.employee_count)

    context = {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_salary": total_salary,
        "average_salary": round(average_salary),
        "department_labels": department_labels,
        "department_counts": department_counts,
    }

    return render(request, "home.html", context)


def login_page(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, f"Welcome {user.username}!")

            return redirect("employee_list")

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


@login_required
def employee_list(request):
    search = request.GET.get("search", "")

    employees = Employee.objects.all()

    if search:
        employees = employees.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(department__name__icontains=search)
        )

    paginator = Paginator(employees, 5)

    page_number = request.GET.get("page")

    employees = paginator.get_page(page_number)

    context = {
        "employees": employees,
        "search": search,
    }

    return render(request, "employee_list.html", context)

@login_required
def export_employee_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="employees.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Employee List")

    y = 760

    employees = Employee.objects.all()

    p.setFont("Helvetica", 12)

    for employee in employees:
        p.drawString(
            50,
            y,
            f"{employee.id} | {employee.name} | {employee.email} | {employee.department} | ₹{employee.salary}"
        )

        y -= 25

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

    p.save()

    return response

@login_required
def export_employee_excel(request):

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Employees"

    sheet.append([
        "ID",
        "Name",
        "Email",
        "Department",
        "Salary"
    ])

    employees = Employee.objects.all()

    for employee in employees:

        sheet.append([
            employee.id,
            employee.name,
            employee.email,
            str(employee.department),
            employee.salary
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="employees.xlsx"'

    workbook.save(response)

    return response


@login_required
def add_employee(request):

    if request.method == "POST":

        # Agar Department ForeignKey hai to pehle Department object lo
        department = Department.objects.get(id=request.POST["department"])

        employee = Employee.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            department=department,
            salary=request.POST["salary"],
            photo=request.FILES.get("photo"),
        )

        # 👇 Employee create hone ke turant baad email bhejna hai
        send_mail(
            subject="Welcome to Our Company",
            message=f"""
Hello {employee.name},

Welcome to our company!

Your details:

Department: {employee.department}
Salary: ₹{employee.salary}

We are happy to have you on our team.

Regards,
HR Team
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.email],
            fail_silently=False,
        )

        messages.success(request, "Employee Added Successfully!")

        return redirect("employee_list")

    context = {
        "departments": Department.objects.all()
    }

    return render(request, "add_employee.html", context)
@login_required
def edit_employee(request, id):

    employee = Employee.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == "POST":

        employee.name = request.POST["name"]
        employee.email = request.POST["email"]

        employee.department = Department.objects.get(
            id=request.POST["department"]
        )

        employee.salary = request.POST["salary"]

        if request.FILES.get("photo"):
            employee.photo = request.FILES.get("photo")

        employee.save()

        messages.success(request, "Employee Updated Successfully!")

        return redirect("employee_list")

    context = {
        "employee": employee,
        "departments": departments,
    }

    return render(request, "edit_employee.html", context)
@login_required
def employee_detail(request, id):

    employee = Employee.objects.get(id=id)

    context = {
        "employee": employee
    }

    return render(request, "employee_detail.html", context)


@login_required
def delete_employee(request, id):

    employee = Employee.objects.get(id=id)

    employee.delete()

    messages.success(request, "Employee Deleted Successfully!")

    return redirect("employee_list")


@login_required
def logout_user(request):

    logout(request)

    messages.success(request, "Logged Out Successfully!")

    return redirect("login")