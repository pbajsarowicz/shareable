import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import (
    ShareableFileSerializer,
    ShareableURLSerializer,
    ShareableRetrieveSerializer,
    UserReportSerializer,
)
from api.mixins import ShareableAPIViewMixin
from shareable.utils import generate_password

logger = logging.getLogger(__name__)


class BaseShareableAPIView(ShareableAPIViewMixin, APIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = generate_password()
            serializer.save(password=password, user=request.user)
            shareable_object = serializer.instance

            logger.info(
                'Added a new %s (uuid: %s)',
                shareable_object.shareable_type.lower(),
                shareable_object.uuid
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.info(
            'Cannot create a shareable object. Errors: %s',
            str(serializer.errors)
        )
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


class ShareableRetrieveAPIView(ShareableAPIViewMixin, APIView):
    permission_classes = ()
    serializer_class = ShareableRetrieveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            logger.info(
                'Accessed a shareable object (uuid: %s)',
                serializer.validated_data['uuid']
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.info(
            'Cannot access a shareable object (uuid: %s). Errors: %s',
            serializer.data['uuid'],
            str(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
