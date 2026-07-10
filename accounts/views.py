from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate


@api_view(["GET"])
def test(request):

    total_users = User.objects.count()

    return Response({
        "message": "Accounts App Working",
        "total_users": total_users
    })
@api_view(["POST"])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            "message": "User Registered Successfully"
        })

    return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):

    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            return Response({
                "message": "Login Successful"
            })

        return Response({
            "message": "Invalid Credentials"
        }, status=401)

    return Response(serializer.errors, status=400)


