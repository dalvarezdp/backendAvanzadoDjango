from django.conf.urls import url

from ui.views import HomePage, ChangeLanguage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name="ui-home"),
    url(r'^change-language/(?P<language>.+)$', ChangeLanguage.as_view(), name="change-language")
]