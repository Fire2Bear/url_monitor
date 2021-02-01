from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from users.models import UserProfile


class ModelFormWithSubmit(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', "Valider", css_class="btn btn-lg btn-primary btn-block bg_main"))
    helper.form_method = 'POST'


class RegisterForm(ModelFormWithSubmit):
    raw_password = forms.CharField(
        label="Mot de passe",
        max_length=256,
        required=True,
        help_text="10 caractères minimum",
        widget=forms.PasswordInput(),
    )

    raw_password_confirmation = forms.CharField(
        label="Mot de passe (confirmation)",
        max_length=256,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'raw_password', 'raw_password_confirmation')


class AccountSettingsForm(ModelFormWithSubmit):

    class Meta:
        model = UserProfile
        fields = ()
