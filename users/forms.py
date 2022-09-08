from django import forms
from users.models import Users


class UserCreationForm(forms.ModelForm):

    class meta:
        model = Users
        fields = '__all__'