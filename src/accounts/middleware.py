class UserAgentUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated is True:
            request.user.update_user_agent(request)

        response = self.get_response(request)

        return response
