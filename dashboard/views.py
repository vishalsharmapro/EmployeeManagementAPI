from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from employee.models import Employee
from django.db.models import Sum,Avg


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

    context = {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_salary": total_salary,
        "average_salary": round(average_salary),
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
            Q(department__icontains=search)
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
def add_employee(request):

    if request.method == "POST":

        Employee.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            department=request.POST["department"],
            salary=request.POST["salary"],
            photo=request.FILES.get("photo")
        )

        messages.success(request, "Employee Added Successfully!")

        return redirect("employee_list")

    return render(request, "add_employee.html")


@login_required
def edit_employee(request, id):

    employee = Employee.objects.get(id=id)

    if request.method == "POST":

        employee.name = request.POST["name"]
        employee.email = request.POST["email"]
        employee.department = request.POST["department"]
        employee.salary = request.POST["salary"]
        if request.FILES.get("photo"):
            employee.photo = request.FILES.get("photo")

        employee.save()

        messages.success(request, "Employee Updated Successfully!")

        return redirect("employee_list")

    context = {
        "employee": employee
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