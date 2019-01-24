from django.forms import ModelForm
from memes.models import OGMeme
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class OGMemeForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = OGMeme
        fields = ['top', 'bottom']

    def clean(self):
        top = self.cleaned_data.get('top')
        bottom = self.cleaned_data.get('bottom')

        if top == ' ':
            top = None

        if bottom == ' ':
            bottom = None

        return self.cleaned_data
