from django.forms import Form, CharField, Textarea
from crispy_forms.layout import Submit, Hidden
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


class OGMemeForm(Form):

    top = CharField(
        label="Top", required=False
    )
    bottom = CharField(
        label="Bottom", required=False
    )

    def __init__(self, *args, **kwargs):
        super(OGMemeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Hidden('flavor', 'og'))
        self.helper.add_input(Submit('submit', 'Create'))

    def clean(self):
        top = self.cleaned_data.get('top')
        bottom = self.cleaned_data.get('bottom')

        if top in [' ', '']:
            top = None

        if bottom in [' ', '']:
            bottom = None

        if not top and not bottom:
            raise ValidationError("top or bottom is required")

        return self.cleaned_data


class TwitMemeForm(Form):

    text = CharField(
        label='Text',
        widget=Textarea(),
    )

    def __init__(self, *args, **kwargs):
        super(TwitMemeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Hidden('flavor', 'twit'))
        self.helper.add_input(Submit('submit', 'Create'))
