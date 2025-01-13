from django.contrib import admin
from django.urls import path
from user.views import login_view, logout_view, register_view
from jobs.views import job_list, job_create, job_detail, delete_job, job_сompany
from resumes.views import create_resume, edit_resume, delete_resume, apply_for_job, user_resume, view_applications

urlpatterns = [
    path('admin/', admin.site.urls),
    #
    path('', job_list, name='job_list'),
    path('job/<int:pk>/', job_detail, name='job_detail'),
    path('job_create/', job_create, name='job_create'),
    path('delete_job/<int:pk>/', delete_job, name='delete_job'),
    #вход пользователя
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='registration'),
    #
    path('job_company/', job_сompany, name='job_сompany'),



    #
    path('my_resume/', user_resume, name='user_resume'),
    path('create_resume/', create_resume, name='create_resume'),
    path('edit_resume/<int:pk>/', edit_resume, name='edit_resume'),
    path('delete_resume/<int:pk>/', delete_resume, name='delete_resume'),
    path('apply_for_job/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('job/<int:job_id>/applications/', view_applications, name='view_applications'),
]
