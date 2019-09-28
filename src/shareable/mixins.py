class StaticContextDataMixin(object):
    static_context_data = {}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(self.static_context_data)

        return context_data
