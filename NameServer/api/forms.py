from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Instance

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Instance
        fields = ('username', 'description', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Instance
        fields = ('username', 'description', 'email')

#class SignupForm(forms.Form):
#    first_name = forms.CharField(max_length=30, label='Voornaam')
#    last_name = forms.CharField(max_length=30, label='Achternaam')
#
#    def signup(self, request, user):
#        user.first_name = self.cleaned_data['first_name']
#        user.last_name = self.cleaned_data['last_name']
#        user.save()