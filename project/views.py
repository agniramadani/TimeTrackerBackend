from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer, Contribution_Serializer
from .models import Project, Project_Contribution
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class Project_CRUD(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Project.objects.all()
        # Reversing the list to display the latest project on top
        serializer = ProjectSerializer(reversed(queryset), many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'message': "Not allowed. You must be a superuser."}, status=403)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        if not request.user.is_superuser:
            return Response({'message': "Not allowed. You must be a superuser."}, status=403)
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'message': 'Text object does not exist'}, status=404)

        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response({'message': "Not allowed. You must be a superuser."}, status=403)
        try:
            text = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'message': 'Text object does not exist'}, status=404)
        text.delete()
        return Response({'message': 'Text object deleted successfully'}, status=204)


class Project_Contribution_CRUD(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        if user_id is None:
            queryset = Project_Contribution.objects.all()
        else:
            queryset = Project_Contribution.objects.filter(user=user_id)
        serializer = Contribution_Serializer(reversed(queryset), many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = Contribution_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            contribution = Project_Contribution.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'message': 'Text object does not exist'}, status=404)

        # Check if the user is either a superuser or the owner of the contribution
        if not (request.user.is_superuser or request.user == contribution.user):
            return Response({'message': 'Permission denied'}, status=403)

        serializer = Contribution_Serializer(contribution, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            contribution = Project_Contribution.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'message': 'Text object does not exist'}, status=404)
        # Check if the user is either a superuser or the owner of the contribution

        if not (request.user.is_superuser or request.user == contribution.user):
            return Response({'message': 'Not allowed'}, status=403)
        contribution.delete()
        return Response({'message': 'Text object deleted successfully'}, status=204)


class SingeContribution(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        queryset = Project_Contribution.objects.filter(project=project_id)
        serializer = Contribution_Serializer(reversed(queryset), many=True)
        return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_total_hours(request, user_id):
    queryset = Project_Contribution.objects.filter(user=user_id)

    total_minutes = 0

    for contribution in queryset:
        total_minutes += contribution.time

    return Response({'total': total_minutes}, status=200)
