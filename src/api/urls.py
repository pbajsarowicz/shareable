from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (
    ShareableFileAPIView,
    ShareableURLAPIView,
    ShareableReportAPIView,
    ShareableRetrieveAPIView,
)
from rest_framework.authtoken import views

urlpatterns = [
    re_path(r'^auth/?', views.obtain_auth_token),
    re_path(r'url/?', ShareableURLAPIView.as_view()),
    re_path(r'file/?', ShareableFileAPIView.as_view()),
    re_path(r'report/?', ShareableReportAPIView.as_view()),
    re_path(r'shareable/?', ShareableRetrieveAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
