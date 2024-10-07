from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from common.urls import router
from common.views import DashboardPage, HomePage, LoginPinRequestView, Logout

urlpatterns = [
    path("wtr-adm/", admin.site.urls),
    re_path(r"api/v1/", include(router.urls)),
    path("login/", LoginPinRequestView.as_view(), name="login-pin-request"),
    path("logout/", Logout.as_view(), name="logout"),
    re_path("^dashboard/", DashboardPage.as_view(), name="dashboard"),
    re_path("^", HomePage.as_view(), name="home"),
    # re_path(
    #     r"^",
    #     include(
    #         ("qr_code.urls", "qr_code"),
    #         namespace="qr_code",
    #     ),
    # ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
