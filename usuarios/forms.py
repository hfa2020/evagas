from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuarios
from django import forms

class MudaUsuarioForm(UserChangeForm):
    password1 = forms.CharField(
        help_text=None,
    )

class CriaUsuariosForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuarios
        # fields = UserCreationForm.Meta.fields + ('',)
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'experiencia', 'ult_escola')


class CriaEmpresaForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuarios
        fields = ('email', 'first_name', 'password1', 'password2')
