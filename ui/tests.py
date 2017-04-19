from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase, Client, override_settings


@override_settings(ROOT_URLCONF="ui.urls")
class HomePageTest(TestCase):

    def test_home_page_for_not_logged_user(self):
        client = Client()
        response = client.get(reverse('ui-home'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Welcome to Instageek</h1>")


@override_settings(ROOT_URLCONF="ui.urls")
class ChangeLanguageTests(TestCase):

    def test_change_language(self):
        client = Client()

        # entramos al home por primera vez
        response = client.get(reverse('ui-home'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Welcome to Instageek</h1>")

        # cambiamos el idioma a castellano
        response = client.get(reverse('change-language', kwargs={'language': 'es'}))
        self.assertEquals(response.status_code, 302)

        # hago una peticion a la url de redireccion
        response = client.get(response.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Bienvenido a Instageek</h1>")

        # cambiamos el idioma a ingles
        response = client.get(reverse('change-language', kwargs={'language': 'en'}))
        self.assertEquals(response.status_code, 302)

        # hago una peticion a la url de redireccion
        response = client.get(response.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Welcome to Instageek</h1>")


@override_settings(ROOT_URLCONF="ui.urls")
class LoginTest(TestCase):

    def test_login_success(self):
        User.objects.create_superuser(username='david', email='david@gmail.com', password='supersegura')

        client = Client()
        response = client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

        response = client.post(reverse('login'), {'username': 'david', 'password': 'supersegura'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, settings.LOGIN_REDIRECT_URL)
