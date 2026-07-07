from django.http import JsonResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    employees = Employee.objects.all()

    data = []

    for emp in employees:
        data.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
            "salary": emp.salary
        })

    return JsonResponse(data, safe=False)


def single_employee(request, id):
    try:
        employee = Employee.objects.get(id=id)

        data = {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary
        }

        return JsonResponse(data)

    except Employee.DoesNotExist:
        return JsonResponse(
            {"message": "Employee not found"},
            status=404
        )


@csrf_exempt
def create_employee(request):
    if request.method == "POST":
        body = json.loads(request.body)
        Employee.objects.create(
            name=body["name"],
            email=body["email"],
            department=body["department"],
            salary=body["salary"]

        )

        return JsonResponse({
              "message": "Employee Created Successfully"
        })

    return JsonResponse({
        "message": "Only POST Request Allowed"
    })
@csrf_exempt
def update_employee(request, id):

    if request.method == "PUT":

        body = json.loads(request.body)

        try:
            employee = Employee.objects.get(id=id)

            employee.name = body["name"]
            employee.email = body["email"]
            employee.department = body["department"]
            employee.salary = body["salary"]

            employee.save()

            return JsonResponse({
                "message": "Employee Updated Successfully"
            })

        except Employee.DoesNotExist:
            return JsonResponse({
                "message": "Employee Not Found"
            }, status=404)

    return JsonResponse({
        "message": "Only PUT Request Allowed"
    })
@csrf_exempt
def delete_employee(request, id):

    if request.method == "DELETE":

        try:
            employee = Employee.objects.get(id=id)

            employee.delete()

            return JsonResponse({
                "message": "Employee Deleted Successfully"
            })

        except Employee.DoesNotExist:
            return JsonResponse({
                "message": "Employee Not Found"
            }, status=404)

    return JsonResponse({
        "message": "Only DELETE Request Allowed"
    })