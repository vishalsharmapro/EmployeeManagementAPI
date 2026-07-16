from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    employees = Employee.objects.all()

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)




@api_view(["GET"])
def single_employee(request, id):
    try:
        employee = Employee.objects.get(id=id)

        serializer =EmployeeSerializer(employee)


        return Response(serializer.data)

    except Employee.DoesNotExist:
        return Response(
            {"message": "Employee not found"},
            status=404
        )


@api_view(["POST"])
def create_employee(request):

    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            "message": "Employee Created Successfully"
        })

    return Response(serializer.errors, status=400)
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