from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import translation
from django.views.generic import CreateView

from ui.models import Post


class HomePage(View):

    @method_decorator(login_required())
    def get(self, request):
        context = {'posts': Post.objects.all().order_by('-id')}
        return render(request, 'ui/home.html', context)


class ChangeLanguage(View):

    def get(self, request, language):
        '''
        Modificamos el LANGUAGE_SESSION_KEY para mantener el idioma en toda la sesion
        :param request:
        :param language:
        :return:
        '''
        request.session[translation.LANGUAGE_SESSION_KEY] = language
        return redirect(request.META.get("HTTP_REFERER", "ui-home"))


class CreatePost(CreateView):

    model = Post
    fields = ["image", "description"]
    template_name = "ui/create-post.html"

    def get_form(self, form_class=None):
        """
        Asignamos al usuario autenticado la propiedad del post
        """
        form = super(CreatePost, self).get_form(form_class)
        form.instance.owner = self.request.user
        return form

    def get_success_url(self):
        """
        Redirige al home si el formulario se guarda correctamente
        """
        return reverse('ui-home')
