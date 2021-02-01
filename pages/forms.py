from pages.models import Page
from users.forms import ModelFormWithSubmit


class NewPageForm(ModelFormWithSubmit):
    class Meta:
        model = Page
        fields = ('title', 'url', )
