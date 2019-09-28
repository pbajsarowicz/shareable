from django import forms

from shareable.models import Shareable


class ShareableAddForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        fields_presence = [
            cleaned_data[field_name] is not None for field_name in self.fields
        ]

        if all(fields_presence):
            self.add_error(None, 'Provide either a file or a URL, not both.')

        if not any(fields_presence):
            self.add_error(None, 'Either a file or a URL must be provided.')

        return cleaned_data

    class Meta:
        model = Shareable
        fields = ('url', 'file')


class ShareableDetailForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        if not Shareable.objects.filter(
            uuid=self.request.resolver_match.kwargs.get('uuid'),
            password=self.cleaned_data['password']
        ).exists():
            self.add_error(None, 'Incorrect password provided')

        return self.cleaned_data['password']
