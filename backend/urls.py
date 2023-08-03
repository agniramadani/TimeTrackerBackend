"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import UserView, login, signup
from project.views import Project_CRUD, Project_Contribution_CRUD, SingeContribution, user_total_hours

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name="Login"),
    path('signup/', signup, name="Signup"),
    path('user/', UserView.as_view(), name='User_Create_Read'),
    path('user/<int:pk>', UserView.as_view(), name='Get_Single_User'),
    path('user/<int:pk>', UserView.as_view(), name='User_Update_Delete'),

    path('project/', Project_CRUD.as_view(), name='Project_Create_Read'),
    path('project/<int:pk>', Project_CRUD.as_view(), name='Project_Update_Delete'),

    path('contribute/', Project_Contribution_CRUD.as_view(), name='Contribute_Create_Read'),
    path('contribute/<int:pk>', Project_Contribution_CRUD.as_view(),
         name='Contribute_Update_Delete'),
    path('userContribution/<int:user_id>', Project_Contribution_CRUD.as_view(), name='User_Contribution'),

    path('projectContributors/<int:project_id>', SingeContribution.as_view(),
         name='Single_Project_Contribution'),
    path('userTotalHours/<int:user_id>', user_total_hours, name='User_Total_Hours')

]
