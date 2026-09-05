from .models import AdminActionLog
from .utils import get_client_ip


class AdminActionLogMiddleware:
    """
    Staff / admin userlarning write requestlarini log qiladi
    """

    WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            user = getattr(request, "user", None)

            # faqat authenticated staff adminlar
            if not user or not user.is_authenticated or not user.is_staff:
                return response

            # faqat write requestlar
            if request.method not in self.WRITE_METHODS:
                return response

            path = request.path or ""

            if path.startswith("/admin/"):
                action = AdminActionLog.ActionChoices.ADMIN_REQUEST
            else:
                action = AdminActionLog.ActionChoices.API_REQUEST

            AdminActionLog.objects.create(
                actor=user,
                action=action,
                method=request.method,
                path=path[:255],
                status_code=getattr(response, "status_code", None),
                ip_address=get_client_ip(request),
                user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:1000],
                extra={
                    "query_params": dict(request.GET),
                },
            )

        except Exception:
            # Audit log hech qachon appni sindirmasligi kerak
            pass

        return response
