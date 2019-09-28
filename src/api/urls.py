from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import ShareableURLAPIView, ShareableFileAPIView, ShareableReportAPIView
from rest_framework.authtoken import views

urlpatterns = [
    re_path(r'url/?', ShareableURLAPIView.as_view()),
    re_path(r'file/?', ShareableFileAPIView.as_view()),
    re_path(r'report/?', ShareableReportAPIView.as_view()),
    re_path(r'^auth/?', views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
