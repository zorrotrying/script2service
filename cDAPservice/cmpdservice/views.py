from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from models import cdap_model, cdap_access

from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage

import os
import subprocess
from shutil import copyfile
import importlib
# Create your views here.

def home(request):
    return render(request, 'author_home.html')



def some_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('type') in ('python', 'r'):
        return True
    else:
        return False

def some_condition2(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('type') in ('python', 'r'):
        return False
    else:
        return True


class RegistModelWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tempscript'))
    template_name = 'modelcore/form_wizard_base.html'

    def dispatch(self, request, *args, **kwargs):
        self.instance = cdap_model()
        return super(RegistModelWizard,self).dispatch(request, *args, **kwargs)

    def get_form_initial(self, step):
        return self.initial_dict.get('0', {'author': self.request.user})

    def get_form_instance(self, step):
        return self.instance

    def done(self, form_list, **kwargs):
        self.instance.save()
        appname = form_list[0].cleaned_data.get('name')
        script_name = form_list[1].cleaned_data['modelpath'].name
        from_script_path = os.path.join(settings.MEDIA_ROOT, 'script4apps', appname, script_name)
        to_script_path = os.path.join(os.path.dirname(__file__),'service_core', appname, '.py' )
        copyfile(from_script_path, to_script_path)
        # open(os.path.join(to_script_path, '__init__.py'), 'w')

        return redirect('app_config', appname=appname)

def configApp(request, appname):
    # demo and test your newly regist service



def runservice(request, appname, *args, **kwargs):
    fun_import = importlib.import_module('%s.%s.py'%('service_core', appname))


    if cdap_model.objects.filter(name=appname).values_list('hasoutput', flat=True)[0]:
        result = fun_import.FunList()
        return JsonResponse(result, safe=False)
    else:
        fun_import.FunList()
        return HttpResponse(status=200)












