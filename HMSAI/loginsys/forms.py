from django import forms
from loginsys.models import Userlogin
from loginsys.models import PointaData11
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class UserloginForm(forms.ModelForm):
    class Meta:
        model = Userlogin
        fields = ['username', 'email', 'password']
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Userlogin.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Userlogin.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists. Please use a different one.")
        return email
    widgets = {
            'password': forms.PasswordInput(),  # Widget for password1 field
        }
                
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class PointaDataForm(forms.ModelForm):
    telephone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="Name must contain only letters and spaces."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    age = forms.IntegerField(
        validators=[
            MinValueValidator(18, message="Age must be a positive number."),
            MaxValueValidator(120, message="Age must be less than or equal to 120.")
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PointaData11
        fields = ['name', 'age', 'doctor', 'time_slot', 'location', 'telephone_number']

    def __init__(self, *args, **kwargs):
        super(PointaDataForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



from loginsys.models import ContactMessages

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessages
        fields = ['name', 'email', 'message']