from django.shortcuts import redirect

# pages that can be opened WITHOUT logging in
OPEN_PREFIXES = ("/login/", "/register/", "/save/", "/check-login/", "/admin/", "/static/")


class LoginRequiredMiddleware:
    """If the visitor is not logged in, send them to the login page first."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.session.get("customer_id")
                and not request.path.startswith(OPEN_PREFIXES)):
            return redirect("login")
        return self.get_response(request)