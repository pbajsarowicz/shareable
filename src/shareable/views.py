import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from shareable.const import ShareableTypes
from shareable.forms import ShareableAddForm, ShareableDetailForm
from shareable.mixins import StaticContextDataMixin
from shareable.models import Shareable
from shareable.utils import generate_password

logger = logging.getLogger(__name__)


class ShareableAddView(StaticContextDataMixin, LoginRequiredMixin, FormView):
    template_name = 'shareable_form.html'
    form_class = ShareableAddForm
    static_context_data = {
        'title': 'Add a shareable link',
        'action_button_text': 'Add',
    }

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        shareable_object = form.save(commit=False)
        password = generate_password()
        shareable_object.password = password
        shareable_object.user = self.request.user
        shareable_object.save()
        self.request.session['password'] = password

        logger.info(
            'Added a new %s (uuid: %s)',
            shareable_object.shareable_type.lower(),
            shareable_object.uuid
        )

        return HttpResponseRedirect(
            reverse('shareable-info', args=(shareable_object.uuid,))
        )


class ShareableInfoView(LoginRequiredMixin, DetailView):
    template_name = 'shareable_info.html'
    model = Shareable
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    context_object_name = 'shareable_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'url': self.request.build_absolute_uri(
                reverse('shareable-detail', args=(self.object.uuid,))
            ),
            'password': self.request.session.get('password')
        })
        return context


class ShareableDetailView(StaticContextDataMixin, FormView):
    template_name = 'shareable_form.html'
    form_class = ShareableDetailForm
    static_context_data = {
        'title': 'Enter a password',
        'action_button_text': 'Get access',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.shareable_object.is_expired:
            context_data['error_message'] = 'The link has expired'

        return context_data

    def form_valid(self, form):
        shareable_object = Shareable.objects.get(
            uuid=self.request.resolver_match.kwargs.get('uuid'),
            password=form.cleaned_data['password']
        )
        shareable_object.views_counter = F('views_counter') + 1
        shareable_object.save()

        logger.info(
            'Accessed the %s (uuid: %s)',
            shareable_object.shareable_type.lower(),
            shareable_object.uuid
        )

        if shareable_object.shareable_type == ShareableTypes.URL:
            return redirect(shareable_object.url)
        return redirect(shareable_object.file.url)

    def get(self, request, uuid, *args, **kwargs):
        self.shareable_object = get_object_or_404(Shareable, uuid=uuid)
        return super().get(request, *args, **kwargs)
