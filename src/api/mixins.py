from django.urls import reverse
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated


class ShareableSerializerMixin(object):

    def save(self, **kwargs):
        self.context['password'] = kwargs['password']
        super().save(**kwargs)

    def to_representation(self, instance):
        return {
            'url': self.context['request'].build_absolute_uri(
                reverse('shareable-detail', args=(instance.uuid,))
            ),
            'password': self.context['password']

        }


class ShareableAPIViewMixin(object):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, instance=None, data=empty, **kwargs):
        assert self.serializer_class is not None, 'Serializer class undefined'
        return self.serializer_class(
            instance=instance, data=data, context=self.get_serializer_context()
        )
