from django.conf.urls import url

from ui.views import HomePage

urlpatterns = [
    url(r'^$', HomePage.as_view(), name="ui-home"),
]