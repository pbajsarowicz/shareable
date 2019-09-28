from base64 import b64encode

from django.core.exceptions import ValidationError
from django.db.models import F
from rest_framework import serializers

from api.fields import Base64FileField
from api.mixins import ShareableSerializerMixin
from shareable.const import ShareableTypes
from shareable.models import Shareable


class ShareableURLSerializer(
    ShareableSerializerMixin, serializers.ModelSerializer
):
    url = serializers.URLField(allow_null=False, allow_blank=False)

    class Meta:
        model = Shareable
        fields = ('url',)


class ShareableFileSerializer(
    ShareableSerializerMixin, serializers.Serializer
):
    ERROR_MESSAGE = 'Value must contain name and extension, e.g. shareable.txt'
    filename = serializers.CharField()
    content = Base64FileField()

    def validate_filename(self, value):
        try:
            filename, extension = value.rsplit('.', 1)
        except ValueError:
            raise ValidationError(self.ERROR_MESSAGE)

        if filename == '' or extension == '':
            raise ValidationError(self.ERROR_MESSAGE)

        return '{}.{}'.format(filename, extension)

    def create(self, validated_data):
        file = self.validated_data['content']
        file.name = self.validated_data['filename']

        return Shareable.objects.create(
            file=file,
            password=validated_data['password'],
            user=validated_data['user']
        )


class UserReportSerializer(serializers.ModelSerializer):
    FIELD_NAMES_MAPPING = {
        ShareableTypes.FILE: 'files',
        ShareableTypes.URL: 'links',
    }

    def to_representation(self, user):
        response = {}

        for item in user.shareables.get_report():
            item_date = str(item['date'])
            response.setdefault(
                item_date,
                {
                    'files': 0,
                    'links': 0
                }
            )
            shareable_type = self.FIELD_NAMES_MAPPING[item['shareable_type']]
            response[item_date][shareable_type] = (
                item['count']
            )

        return response


class ShareableRetrieveSerializer(serializers.Serializer):
    ERROR_MESSAGE = (
        'Shareable object not found or provided an incorrect password'
    )
    uuid = serializers.UUIDField()
    password = serializers.CharField()

    def validate(self, validated_data):
        if not Shareable.objects.filter(
            uuid=validated_data['uuid'],
            password=validated_data['password']
        ).exists():
            raise ValidationError(self.ERROR_MESSAGE)

        return validated_data

    def to_representation(self, validated_data):
        shareable_object = Shareable.objects.get(
            uuid=validated_data['uuid'],
            password=validated_data['password']
        )
        shareable_object.views_counter = F('views_counter') + 1
        shareable_object.save()

        if shareable_object.shareable_type == ShareableTypes.URL:
            content = shareable_object.url
        else:
            with shareable_object.file as file:
                content = b64encode(file.read()).decode()

        return {
            'content': content,
            'type': shareable_object.shareable_type
        }
