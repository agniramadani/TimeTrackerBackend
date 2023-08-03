from project.models import Project, Project_Contribution
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


# Project Test
class ProjectViewTestCase(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'user1', 'password': 'pass1', "is_superuser": "True"}
        self.create_user_response = self.client.post('/user/', self.user_data)
        login_response = self.client.post('/login/', self.user_data)
        # Add the token to the request headers for authentication
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Get the user instance from the database
        self.user = User.objects.get(username=self.create_user_response.data['username'])
        # Create projects
        self.project1 = Project.objects.create(user=self.user, title="Project Title1")
        self.project2 = Project.objects.create(user=self.user, title="Project Title2")
        # Create Contributions
        self.contribution1 = Project_Contribution.objects.create(user=self.user, project=self.project1, time=10,
                                                                 create_date="2023-08-01")
        self.contribution2 = Project_Contribution.objects.create(user=self.user, project=self.project2, time=20,
                                                                 create_date="2023-08-01")

    def test_get_all(self):
        # Send a GET request to retrieve all project
        response = self.client.get('/project/')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Two records must be in the db
        self.assertEqual(Project.objects.count(), 2)

    def test_create(self):
        # Send a POST request to create a new project
        create_response = self.client.post('/project/', {"user": self.user.id, "title": "Project Title1"})
        # Check if the response status code is 201 (Created)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        # Send a PUT request to change title of project 1
        put_response = self.client.put(f'/project/{self.project1.id}', {"title": "New Title"})
        # Check if status is OK
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        # Check if the title is changed
        self.assertEqual(put_response.data['title'], 'New Title')

    def test_delete(self):
        # Send a DELETE request to delete project 2
        put_response = self.client.delete(f'/project/{self.project2.id}')
        # Check if status is No Content
        self.assertEqual(put_response.status_code, status.HTTP_204_NO_CONTENT)


# Contribute Test
class ContributeViewTestCase(ProjectViewTestCase):
    def test_get_all_contributions(self):
        # Send a GET request to retrieve all contributions
        response = self.client.get('/contribute/')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Two records must be in the db
        self.assertEqual(Project.objects.count(), 2)

    def test_get_all(self):
        # Send a GET request to retrieve all contributions
        response = self.client.get('/contribute/')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Two records must be in the db
        self.assertEqual(Project.objects.count(), 2)

    def test_project_contribution(self):
        # Send a GET request to retrieve all the project contributions
        response = self.client.get(f'/projectContributors/{self.project1.id}')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        # Send a POST request to create a new contribution
        create_response = self.client.post('/contribute/', {"user": self.user.id, "project": self.project1.id,
                                                            "time": 20, "create_date": "2023-08-01"})
        # Check if the response status code is 201 (Created)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        # Send a PUT request to change title of contribution 1
        put_response = self.client.put(f'/contribute/{self.contribution1.id}', {"time": 30})
        # Check if status is OK
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        # Check if the title is changed
        self.assertEqual(put_response.data['time'], 30)

    def test_delete(self):
        # Send a DELETE request to delete contribution 2
        put_response = self.client.delete(f'/contribute/{self.contribution2.id}')
        # Check if status is No Content
        self.assertEqual(put_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_total_hours(self):
        # Send a GET request to retrieve the total hours associated with the user.
        response = self.client.get(f'/userTotalHours/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
