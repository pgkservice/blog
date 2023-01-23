from django import forms
from .models import Contact, Subscriber



class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class':'text-input',
                                                            'placeholder' : 'Enter Email Address',
                                                            'style': 'text-align'}))




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'website', 'location', 'subject', 'message']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control',
                                            'style': 'max-width: 300px;'
                                                     'text-align:center;'
                                                     'margin:auto;',
                                            'placeholder': 'Name'
                                            }),
            'email': forms.EmailInput(attrs={'class' : 'form-control',
                                              'style': 'max-width: 300px;'
                                                       'text-align:center;'
                                                       'margin:auto;',
                                              'placeholder': 'Email'
                                              }),
            'website': forms.TextInput(attrs={'class' : 'form-control',
                                               'style': 'max-width: 300px;'
                                                        'text-align:center;'
                                                        'margin:auto;',
                                               'placeholder': 'Website'
                                               }),
            'location': forms.TextInput(attrs={'class' : 'form-control',
                                                'style': 'max-width: 300px;'
                                                         'text-align:center;'
                                                         'margin:auto;',
                                                'placeholder': 'Location'
                                                }),
            'subject': forms.TextInput(attrs={'class' : 'form-control',
                                               'style': 'max-width: 300px;'
                                                        'text-align:center;'
                                                        'margin:auto;',
                                               'placeholder': 'Subject'
                                               }),
            'message': forms.Textarea(attrs={'class':'form-control',
                                              'placeholder': 'Message',
                                             'style': 'text-align: center;'
                                              })
        }
