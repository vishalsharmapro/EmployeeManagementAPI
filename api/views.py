from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from employee.models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter




@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

class EmployeeListCreateAPIView(generics.ListCreateAPIView):

    queryset = Employee.objects.all()

    serializer_class = EmployeeSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "department",
    ]

    search_fields = [
        "name",
        "email",
    ]

    ordering_fields = [
        "salary",
        "name",
        "id",
    ]
class EmployeeRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Employee.objects.all()

    serializer_class = EmployeeSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "id"