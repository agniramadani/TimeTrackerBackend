from rest_framework import serializers
from .models import Project, Project_Contribution


class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'user', 'title', 'create_date', 'username')

    def get_username(self, obj):
        return obj.user.username


class Contribution_Serializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()

    class Meta:
        model = Project_Contribution
        fields = ('id', 'user', 'username', 'project', 'project_title', 'time', 'comment', 'create_date',)

    def get_username(self, obj):
        return obj.user.username

    def get_project_title(self, obj):
        return obj.project.title
