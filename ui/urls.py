from django.conf.urls import url
from django.contrib.auth.views import LoginView

from ui.views import HomePage, ChangeLanguage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name="ui-home"),
    url(r'^login$', LoginView.as_view(template_name="ui/login.html"), name="login"),
    url(r'^change-language/(?P<language>.+)$', ChangeLanguage.as_view(), name="change-language")
]