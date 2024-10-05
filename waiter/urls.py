from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from common.urls import router
from common.views import HomePage

urlpatterns = [
    path("wtr-adm/", admin.site.urls),
    re_path(r"api/v1/", include(router.urls)),
    re_path(
        r"app/",
        include(
            ("common.urls", "common"),
            namespace="common",
        ),
    ),
    # path("api/v2/login/", LoginAPIView.as_view(), name="login"),
    # path("logout/", Logout.as_view(), name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
