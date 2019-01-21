from django import forms
from django.forms import ModelForm
from memes.models import OGMeme
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class OGMemeForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = OGMeme
        fields = ['top', 'bottom']

    def clean(self):
        top = self.cleaned_data.get('top')
        bottom = self.cleaned_data.get('bottom')
        if not top and not bottom:
            raise forms.ValidationError('Top or Bottom text is required')
        return self.cleaned_data
