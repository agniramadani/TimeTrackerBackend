
# Time Tracker API

The API offers a flexible and efficient way to manage working hours, making it easy for users to keep track of their contributions to each project.

## Roadmap

- Installation
- Starting development server
- User Component
- Project Component
- API Requests




## Installation

Before getting started with Django, it's essential to have Python3 installed on your system, preferably a version > 3.6.

- Download python3: https://www.python.org/

- Clone the repository onto your local machine.

- Open the project.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment for MacOS or Linux

```bash
. bin/activate
```

Activate the virtual environment for Windows:
```bash
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```


## Starting development server
Before running the Django server, it's essential to apply any pending migrations to update the database schema. 

Use the following command:
```bash
python3 manage.py migrate
```

If you make any changes to your models, such as adding a new model or modifying existing ones, you need to create new migrations to capture those changes. 

Use the following commands:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

The application will be running on port 8000.
```bash
python3 manage.py runserver
```

## User Component
In this application we have:
- Superuser (Admin)
- User

Create a superuser:
```bash
python3 manage.py createsuperuser
```

You can use the Django dashboard at http://localhost:8000/admin. The dashboard provides a user-friendly interface for management.

## Project Component
Only the Superuser (Admin) can create and manage projects.
Users can see in which project they have worked on.


### Project Contribution
Users enter their project contribution time, which is saved in minutes. Additionally, they can provide an optional comment.

Superuser (Admin) or the User (Contributor) can CRUD.


 



## API Requests

Use [Postman](https://www.postman.com/) or other tools for making HTTP requests.

### Get Users
Retreive the list of users.
- Method `[GET]` endpoint: `/user/`

### Create User

- Method `[POST]` endpoint: `/user/` 

`username` and `password` are required!

 `is_superuser` by default is false.
```
{
    "username": "user1",
    "password": "pass1",
    "first_name": "",
    "last_name": "",
    "email": "",
    "is_superuser": true
} 
```
### Update User
- Method `[PUT]` endpoint: `/user/id`
Enpoint includes the user id of the user you want to update.

Specify the field you want to update (e.g., first_name).

```
{
    "first_name": "User1",
} 
```

### Delete User
- Method `[DELETE]` endpoint: `/user/id`
Enpoint includes the user id of the user you want to delete.

### Signup
`username` and `password` are required!
- Method `[POST]` endpoint: `/signup/`
```
{
    "username": "user1",
    "password": "pass1",
    "first_name": "",
    "last_name": "",
    "email": "",
} 
```
After a successful signup, you'll receive an object with the token and user details.
### Login
- Method `[POST]` endpoint: `/login/`
```
{
    "username": "user",
    "password": "pass",
} 
```
After a successful login, you'll receive an object with the token and user details.

### Get Projects
For any project request user must be authenticated! 

If you are using Postman then in Headers add a new key: `Authorization` value ex: `token d48e91672d1ac0138ee173755b125269ab26da8b`

Retreive the list of project.
- Method `[GET]` endpoint: `/project/`

### Create Project
- Method `[POST]` endpoint: `/project/` 

`user` is required!

 `create_date` by default is current date.
```
{
    "user": user_id,
    "title": "Project",
} 
```
### Update Project
- Method `[PUT]` endpoint: `/project/id`
Enpoint includes the project id to update.

```
{
    "title": "Project1",
} 
```

### Delete Project
- Method `[DELETE]` endpoint: `/project/id`
Enpoint includes the project id to delete.


### Get Project Contributions
For any project contribution request user must be authenticated!

Retreive the list of contribution.
- Method `[GET]` endpoint: `/contribute/`

### Create Project Contribution
- Method `[POST]` endpoint: `/contribute/` 

`user_id` and `project_id` are required!

```
{
    "user": user_id,
    "project": project_id,
    "time": 30,
    "comment": "",
    "create_date": "YYYY-MM-DD"
} 
```
### Update Project Contribution
- Method `[PUT]` endpoint: `/contribute/id`
Enpoint includes the contribution id to update.

```
{
    "time": 50,
} 
```

### Delete Project Contribution
- Method `[DELETE]` endpoint: `/contribute/id`
Enpoint includes the contribution id to delete.

### Get User Contribution
Authentication is required!
- Method `[GET]` endpoint: `/userContribution/user_id`

### Get Project Contribution
Authentication is required!
- Method `[GET]` endpoint: `/projectContributors/project_id`

### Get User Total Hours
Authentication is required!
- Method `[GET]` endpoint: `/userTotalHours/user_id`

## Unit Testing
Unit tests are designed to validate the correctness of small units of code in isolation, ensuring that each function, method, or class behaves as expected. 

In this API, we have unit testing for each component.

To execute the unit tests:
```bash
python3 manage.py test
```

## Author

- [Agni Ramadani](https://github.com/agniramadani)
