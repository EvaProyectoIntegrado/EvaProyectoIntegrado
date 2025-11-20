from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña'
    )
    password_confirmacion = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Contraseña'
    )
    rol = forms.ChoiceField(
        choices=Perfil.ROLES,
        label='Rol'
    )

    def __init__(self, *args, **kwargs):
        """Aplica clases de Bootstrap automáticamente a todos los campos."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            existing_classes = widget.attrs.get('class', '')
            # Evita duplicar clases
            if 'form-control' not in existing_classes:
                widget.attrs['class'] = (existing_classes + ' form-control').strip()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmacion']

    def clean_password_confirmacion(self):
        """Valida que las contraseñas coincidan."""
        password = self.cleaned_data.get('password')
        password_confirmacion = self.cleaned_data.get('password_confirmacion')

        if password and password_confirmacion and password != password_confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password_confirmacion