from django.urls import path
from shareable.views import (
    ShareableAddView, ShareableInfoView, ShareableDetailView
)


urlpatterns = [
    path('', ShareableAddView.as_view()),
    path('info/<uuid>/', ShareableInfoView.as_view(), name='shareable-info'),
    path(
        'shareable/<uuid>/',
        ShareableDetailView.as_view(),
        name='shareable-detail'
    ),
]
