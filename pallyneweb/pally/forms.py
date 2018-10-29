from django import forms
from pally.models import LearnerProfile, PallyneUser, Publisher
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = PallyneUser
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cleaned = self.cleaned_data
        if cleaned['password2'] != cleaned['password']:
            raise forms.ValidationError('Passwords don\'t match')
        return cleaned['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("This field is required")
        if PallyneUser.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("This Email is taken already! ")
        return self.cleaned_data['email']

    def save(self, request):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.is_active = False
        user.set_password(UserRegistrationForm.clean_password2(self))
        user.save()

        context = {
        'request': request,
        'protocol': request.scheme,
        'username': self.cleaned_data.get('username'),
        'domain': request.META['HTTP_HOST'],
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),

        }
        subject = 'Pallyne account activation'
        email = render_to_string('registration/email/activation_email.txt', context)
        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user

class PallyUserEditForm(forms.ModelForm):
    class Meta:
        model = PallyneUser
        fields =('first_name', 'last_name', 'email')

class PallyLearnerProfileEditForm(forms.ModelForm):
    class Meta:
        model = LearnerProfile
        fields = ('facebook_link', 'twitter_link', 'institution', 'country_name', 'profile_photo')

class PallyPublisherProfileEditForm(forms.ModelForm):
    model = Publisher
    fields = ('publisher_name', 'website', 'publisher_logo')
