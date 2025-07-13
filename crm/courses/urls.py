# courses/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("courses/",       views.CourseListView.as_view(),  name="course-list"),
    path("courses/add/",   views.course_create, name="course-add"),
]
