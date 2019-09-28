from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ShareableURLSerializer, ShareableFileSerializer, UserReportSerializer
from api.mixins import ShareableAPIViewMixin
from shareable.utils import generate_password


class BaseShareableAPIView(ShareableAPIViewMixin, APIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = generate_password()
            serializer.save(password=password, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareableURLAPIView(BaseShareableAPIView):
    serializer_class = ShareableURLSerializer


class ShareableFileAPIView(BaseShareableAPIView):
    serializer_class = ShareableFileSerializer


class ShareableReportAPIView(ShareableAPIViewMixin, APIView):
    serializer_class = UserReportSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
