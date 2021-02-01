from users.forms import ModelFormWithSubmit
from verifications.models import Verification


class NewVerificationForm(ModelFormWithSubmit):

    class Meta:
        model = Verification
        fields = ('page', 'verification_type', 'verification_option', )
