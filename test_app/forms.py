from django import forms
from .models import *

class MemberForm(forms.Form):
    member = forms.ModelChoiceField(Member.objects,  label='', empty_label='選択してください', to_field_name='name')


class VisitorsForm(forms.ModelForm):
    class Meta:
        model = Visitors
        fields = ('date', 'time', 'company_name', 'visitor_name', 'temperature',
                'accompany1_name', 'accompany1_temp', 'accompany2_name', 'accompany2_temp',
                'accompany3_name', 'accompany3_temp', 'position', 'interviewer', 'content',
                'is_contacted')
        labels={
           'date':'',
           'time':'',
           'company_name':'',
           'visitor_name': '',
           'temperature': '',
           'accompany1_name': '',
           'accompany1_temp': '',
           'accompany2_name': '',
           'accompany2_temp': '',
           'accompany3_name': '',
           'accompany3_temp': '',
           'position': '',
           'interviewer': '',
           'content': '',
           'is_contacted': '',
           }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact', 'interviewer', 'time', 'contents')
        labels = {
            'contact': '',
            'interviewer': '',
            'time': '',
            'contents': '',
        }