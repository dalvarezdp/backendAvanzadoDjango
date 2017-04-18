from django.test import TestCase, Client, override_settings


@override_settings(ROOT_URLCONF="ui.urls")
class HomePageTest(TestCase):

    def test_home_page_for_not_logged_user(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Welcome to Instageek</h1>")
