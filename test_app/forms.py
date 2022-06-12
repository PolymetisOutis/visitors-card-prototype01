from django import forms
from .models import *

class MemberForm(forms.Form):
    member = forms.ModelChoiceField(Member.objects,  label='', empty_label='選択してください', to_field_name='name', required=False)


class VisitorsForm(forms.ModelForm):
    class Meta:
        model = Visitors
        fields = ('date', 'time', 'company_name', 'visitor_name', 'temperature',
                'accompany1_name', 'accompany1_temp', 'accompany2_name', 'accompany2_temp',
                'accompany3_name', 'accompany3_temp', 'position', 'interviewer', 'content')
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
        #    'is_contacted': '',
           }


class ContactForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     # first call parent's constructor
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     # there's a `fields` property now
    #     # for key in self.fields.keys():
    #     #     self.fields[key].required = False
    #     self.fields['interviewer'].required = False
    #     self.fields['time'].required = False
    #     self.fields['contents'].required = False
    # time = forms.TimeField(required=False)
    # contents = forms.CharField(widget=forms.Textarea, required=False) 
    class Meta:
        model = Contact
        fields = ('interviewer', 'time', 'contents')
        labels = {
            'interviewer': '',
            'time': '',
            'contents': '',
        }

        # fields = ('contact', 'interviewer', 'time', 'contents')
        # labels = {
        #     'contact': '',
        #     'interviewer': '',
        #     'time': '',
        #     'contents': '',
        # }