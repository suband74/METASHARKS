"""university URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from studies.api import (
    StudentsApiView,
    GroupOperationsViewSet,
    FacultyApiView,
    StudentViewSet,
    MassComplectationGroup,
    Report,
    ReportGroups
)

router = DefaultRouter()
router.register("groups", GroupOperationsViewSet, basename="groups")
router.register("student_in_group", StudentViewSet, basename="student_in_group")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("api/v1/students", StudentsApiView.as_view()),
    path("api/v1/faculty", FacultyApiView.as_view()),
    path("api/v1/mass_students", MassComplectationGroup.as_view()),
    path("api/v1/report", Report.as_view()),
    path("api/v1/report_groups", ReportGroups.as_view()),
    path("api/v1/", include(router.urls), name="api"),
]
