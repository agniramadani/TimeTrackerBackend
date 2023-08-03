from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserViewTestCase(APITestCase):
    def setUp(self):
        # Set up any required data for the test cases
        self.user_data = {'username': 'user1', 'password': 'pass1'}

    def test_get_single_user(self):
        # Create a user instance in the database
        user = User.objects.create(username='user1', password='pass1')
        # Send a GET request to retrieve the user using its primary key
        response = self.client.get(f'/user/{user.id}')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the username is the same
        self.assertEqual(response.data['username'], user.username)

    def test_get_all_users(self):
        # Create multiple user instances in the database
        User.objects.create(username='user1', password='pass1')
        User.objects.create(username='user2', password='pass2')

        # Send a GET request to retrieve all users
        response = self.client.get('/user/')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the returned data matches the serialized data of all users
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        # Send a POST request to create a new user
        create_response = self.client.post('/user/', self.user_data)

        # Check if the response status code is 201 (Created)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Check if the user was created in the database
        self.assertEqual(User.objects.count(), 1)

        # Try to log in with the created user
        login_response = self.client.post('/login/', self.user_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)
        self.assertIn('user', login_response.data)

    def test_create_user_invalid_data(self):
        # Send a POST request with invalid data (missing password) to create a new user
        response = self.client.post('/user/', {'username': 'user1'})

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the user was not created in the database
        self.assertEqual(User.objects.count(), 0)

    def test_put_valid_data(self):
        user = User.objects.create(username='user1', password='pass1')
        # Send a PUT request with valid data and change username from user1 -> user5
        response = self.client.put(f'/user/{user.id}', {'username': 'user5'})
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if username is updated correctly
        self.assertEqual(response.data['username'], 'user5')

    def test_put_invalid_data(self):
        user = User.objects.create(username='user1', password='pass1')
        # Send a PUT request with invalid data, username must not have any empty spaces.
        response = self.client.put(f'/user/{user.id}', {'username': 'new username'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_user(self):
        user = User.objects.create(username='user1', password='pass1')
        # Send a DELETE request
        response = self.client.delete(f'/user/{user.id}')
        # Check if the user is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_user(self):
        # Send a DELETE request
        response = self.client.delete(f'/user/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_signup(self):
        # Send a POST request with valid data for signing up
        response = self.client.post('/signup/', self.user_data)

        # Assert the response status code and the response data
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_unsuccessful_signup(self):
        # Send a POST request with invalid data, password is missing
        response = self.client.post('/signup/', {'username': 'user1'})

        # For invalid data we show 400
        self.assertEqual(response.status_code, 400)
