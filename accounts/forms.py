from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

class CustomErrorList(ErrorList):
    """
    Custom error list that renders each error as a Bootstrap alert.
    """
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
        f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form that customizes the default Django UserCreationForm.
    It removes the default help texts for 'username', 'password1', and 'password2'
    and adds Bootstrap styling to these fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
