from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Department
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def department_list(request):
    departments = Department.objects.all()

    context = {
        "departments": departments
    }

    return render(request, "department_list.html", context)


@login_required
def add_department(request):

    if request.method == "POST":

        Department.objects.create(
            name=request.POST["name"]
        )

        messages.success(request, "Department Added Successfully!")

        return redirect("department_list")

    return render(request, "add_department.html")
@login_required
def edit_department(request, id):

    department = Department.objects.get(id=id)

    if request.method == "POST":

        department.name = request.POST["name"]
        department.save()

        messages.success(request, "Department Updated Successfully!")

        return redirect("department_list")

    context = {
        "department": department
    }

    return render(request, "edit_department.html", context)
@login_required
def delete_department(request, id):

    department = Department.objects.get(id=id)

    department.delete()

    messages.success(request, "Department Deleted Successfully!")

    return redirect("department_list")