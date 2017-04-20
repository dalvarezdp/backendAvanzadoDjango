from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import translation

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
