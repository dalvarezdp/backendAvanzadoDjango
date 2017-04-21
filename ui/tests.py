from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from django.test import TestCase, Client, override_settings

from ui.models import Post


@override_settings(ROOT_URLCONF="ui.urls")
class HomePageTest(TestCase):

    def test_home_page_for_not_logged_user(self):
        client = Client()
        response = client.get(reverse('ui-home'))
        self.assertEquals(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response.url)  # login in /login?next=/

    def test_home_page_for_logged_user(self):
        user = User.objects.create(username='david')
        client = Client()
        client.force_login(user)  # autenticamos al usuario
        response = client.get(reverse('ui-home'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<h1>Welcome to Instageek</h1>")

    def test_home_has_posts(self):
        user = User.objects.create(username="chewbacca")
        posts = [
            Post(owner=user, image=File(None), description="Post1"),
            Post(owner=user, image=File(None), description="Post2"),
            Post(owner=user, image=File(None), description="Post3"),
            Post(owner=user, image=File(None), description="Post4")
        ]
        Post.objects.bulk_create(posts)

        # creamos un cliente
        client = Client()
        client.force_login(user)
        response = client.get(reverse('ui-home'))
        self.assertEqual(response.status_code, 200)

        # comprobamos que la descripcion de todos los posts aparece en la respuesta del home
        for post in posts:
            self.assertContains(response, post.description)

    def test_home_has_no_posts(self):
        user = User.objects.create(username="chewbacca")
        client = Client()
        client.force_login(user)  # autenticamos al usuario
        response = client.get(reverse('ui-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts here.")


@override_settings(ROOT_URLCONF="ui.urls")
class ChangeLanguageTests(TestCase):

    def test_change_language(self):

        user = User.objects.create(username='david')

        client = Client()
        client.force_login(user)    #autenticamos al usuario

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

    def setUp(self):
        self.username = 'david'
        self.email = 'david@gmail.com'
        self.password = 'supersegura'

        User.objects.create_superuser(username=self.username, email=self.email, password=self.password)

        self.client = Client()
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, settings.LOGIN_REDIRECT_URL)

    def test_login_failed(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': 'pass erronea'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Your username and password didn't match. Please try again.")


@override_settings(ROOT_URLCONF="ui.urls")
class CreatePostTest(TestCase):

    def test_not_logged_user_is_sent_to_login_page(self):
        client = Client()
        response = client.get(reverse('create-post'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_REDIRECT_URL in response.url)

    def test_create_post(self):
        user = User.objects.create(username='david')

        client = Client()
        client.force_login(user)  # autenticamos al usuario

        # ir a la pagina del formulario de creacion
        response = client.get(reverse('create-post'))
        self.assertEquals(response.status_code, 200)

        # enviar el formulario
        response = client.post(reverse('create-post'), {
            'image': SimpleUploadedFile("post.jpg", "image data".encode(), content_type="image/jpeg"),  # archivo fake
            'description': 'Test'
        })

        # comprobar que se ha creado correctamente el post en la base de datos
        self.assertEqual(1, Post.objects.all().count())

        post = Post.objects.all().last()
        self.assertEqual(post.owner, user)
        self.assertEqual(post.description, 'Test')
