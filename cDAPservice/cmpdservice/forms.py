from django import forms
from models import cdap_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions


class CDAP_model_form1(forms.ModelForm):

    class Meta:
        model = cdap_model
        exclude = ('pub_date', 'slug', 'modelpath', 'modelcmd',)

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(CDAP_model_form1, self).__init__(*args, **kwargs)
        self.fields['author'].widget = HiddenInput()

        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            ))

class CDAP_model_form2(forms.ModelForm):
    class Meta:
        model = cdap_model
        fields = ('modelpath',)

    def __init__(self, *args, **kwargs):
        super(CDAP_model_form2, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            ))

class CDAP_model_form3(forms.ModelForm):

    class Meta:
        model = cdap_model
        fields = ('modelcmd', )

    def __init__(self, *args, **kwargs):
        super(CDAP_model_form3, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                                href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            ))


class Arg_type_form(forms.Form):
    def __init__(self, *args, **kwargs):
        ArgList = kwargs.pop('ArgList')
        super(Arg_type_form, self).__init__(*args, **kwargs)

        arg_type_class = (
            ('FileField', 'File'),
            ('CharField', 'String'),
            ('FloatField', 'Float'),
            ('IntegerField', 'Integer'),
            ('DateField', 'Date'),
            ('BooleanField', 'Boolean'),
        )

        for x in xrange(len(ArgList)):
            self.fields[ArgList[x]] = forms.ChoiceField(
                label=ArgList[x],
                choices=arg_type_class,
                required=True,
            )

