from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from ui.views import HomePage, ChangeLanguage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name="ui-home"),
    url(r'^login$', LoginView.as_view(template_name="ui/login.html"), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
    url(r'^change-language/(?P<language>.+)$', ChangeLanguage.as_view(), name="change-language")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
