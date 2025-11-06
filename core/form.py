from django import forms
from core.models import CustomUser, Assessment

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['favorite_subject','strength','interest','classified']
        exclude =['created_at']

        widgets={
            'favorite_subject': forms.TextInput(attrs={
                'id':'favorite',
                'class': 'form-control'
            }),
            'classified': forms.Select(attrs={
                'id': 'classfied',
                'class': 'form-control'
            }),
            'strength': forms.Select(attrs={
                'id':'strength-select',
                'class': 'form-control'
            }),
            'interest': forms.Select(attrs={
                'id':'interest-select',
                'class': 'form-control'
            })
        }

class CustomUserForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  # enables native date picker
            'class': 'form-control'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'phone', 'dp', 'dob', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exist!")
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            increase_value = 1
            new_username = f'{username}{increase_value}'

            while CustomUser.objects.filter(username=username).exists():
                increase_value += 1
            raise forms.ValidationError(f"This username:{username} already exist. Try {new_username} instead.")
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This mobile number already exist!")
        return phone
