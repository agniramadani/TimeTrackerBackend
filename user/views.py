from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404


class UserView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=404)

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=404)
        user.delete()
        return Response({'message': 'The user has been successfully deleted.'}, status=204)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if both username and password are provided in the request
    if not username or not password:
        return Response({"error": "Both username and password are required."}, status=400)

    # Authenticate the user using the provided username and password
    user = authenticate(username=username, password=password)

    # If the provided credentials are valid
    if user is not None:
        # Create or retrieve a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Serialize the user data and send the response
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data})

    # If the provided credentials are invalid
    return Response({"error": "Invalid username or password."}, status=401)


@api_view(['POST'])
def signup(request):
    # Create a mutable copy of the QueryDict
    data = request.data.copy()

    # Convert the username to lowercase and save it in the data
    data['username'] = data['username'].lower()

    # Create a serializer instance using the provided request data
    serializer = UserSerializer(data=data)

    # Check if the data provided in the request is valid
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=data['username'])

        # Create a token for the user
        token = Token.objects.create(user=user)

        # Return the token and serialized user data in the response
        return Response({"token": token.key, "user": serializer.data})

    # If the provided data is invalid
    return Response(serializer.errors, status=400)
