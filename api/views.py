from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from employee.models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404
@api_view(["GET", "POST"])
def employee_list_api(request):

    if request.method == "GET":

        employees = Employee.objects.all()

        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data)

    elif request.method == "POST":

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "PUT", "DELETE"])
def employee_detail_api(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "GET":

        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)

    elif request.method == "PUT":

        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "DELETE":

        employee.delete()

        return Response(

            {"message": "Employee deleted successfully"},

            status=status.HTTP_200_OK

        )