from django.shortcuts import render, redirect
from django.views import View
from django.utils import translation


class HomePage(View):

    def get(self, request):
        return render(request, 'ui/home.html')


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
