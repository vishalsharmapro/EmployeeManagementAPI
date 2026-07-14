from rest_framework.decorators import api_view
from rest_framework.response import Response

from employee.models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def employee_list_api(request):

    employees = Employee.objects.all()

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)
@api_view(["GET"])
def employee_detail_api(request, id):

    employee = get_object_or_404(Employee, id=id)

    serializer = EmployeeSerializer(employee)

    return Response(serializer.data)