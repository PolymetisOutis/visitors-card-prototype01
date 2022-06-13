from turtle import position
from django.shortcuts import get_object_or_404, render
from .models import *
from django.urls import reverse_lazy
from .forms import ContactForm, MemberForm, VisitorsForm
from django.views.generic import UpdateView
from django import forms
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def index(request):
    context = {
        'msg': 'Hello, world!!',
    }
    return render(request, 'test_app/index.html', context)


def welcome(request):
    context = {
        'msg': 'ようこそ！！'
    }
    return render(request, 'test_app/entry_form/welcome.html', context)


def confirm(request):
    if request.method == 'POST':
        context = {
            'date': request.POST.get('date'),
            'time': request.POST.get('time'),
            'company_name': request.POST.get('company_name'),
            'visitor_name': request.POST.get('visitor_name'),
            'temperature': request.POST.get('temperature'),
            'accompany1_name': request.POST.get('accompany1_name'),
            'accompany1_temp': request.POST.get('accompany1_temp'),
            'accompany2_name': request.POST.get('accompany2_name'),
            'accompany2_temp': request.POST.get('accompany2_temp'),
            'accompany3_name': request.POST.get('accompany3_name'),
            'accompany3_temp': request.POST.get('accompany3_temp'),
            'position': request.POST.get('position'),
            'interviewer': request.POST.get('interviewer'),
            'content': request.POST.get('content'),
        }
    return render(request, 'test_app/confirm.html', context)


def sent(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        company_name = request.POST.get('company_name')
        visitor_name = request.POST.get('visitor_name')
        temperature = request.POST.get('temperature')
        accompany1_name = request.POST.get('accompany1_name')
        accompany1_temp = request.POST.get('accompany1_temp')
        accompany2_name = request.POST.get('accompany2_name')
        accompany2_temp = request.POST.get('accompany2_temp')
        accompany3_name = request.POST.get('accompany3_name')
        accompany3_temp = request.POST.get('accompany3_temp')
        position = request.POST.get('position')
        interviewer = request.POST.get('interviewer')
        content = request.POST.get('content')

        Visitors.objects.create(date=date, time=time, company_name=company_name, visitor_name=visitor_name,
        temperature=temperature, accompany1_name=accompany1_name, accompany1_temp=accompany1_temp, accompany2_name=accompany2_name,
        accompany2_temp=accompany2_temp, accompany3_name=accompany3_name, accompany3_temp=accompany3_temp, position=position,
        interviewer=interviewer, content=content)
    return render(request, 'test_app/lazy/thankyou.html')


def history(request):
    visitors = Visitors.objects.all()
    context = {
        'visitors': visitors,
    }
    visitor_type = Visitors.objects.all().values_list('visitor_name', flat=True).order_by('visitor_name').distinct()
    print(visitor_type)
    visitor_type1 = visitor_type.get(visitor_name='小川')
    print(visitor_type1)
    return render(request, 'test_app/history.html', context)


def detail(request, pk):
    visitor = Visitors.objects.get(pk=pk)
    print(visitor.is_contacted)
    if visitor.is_contacted:
        # contact = visitor.contact_set.all()
        contact = Contact.objects.filter(contact__pk=pk)[0]
        context = {
            'visitor': visitor,
            'contact': contact,
        }
        print(contact)
    else:
        form = MemberForm()
        context = {
            'visitor': visitor,
            'form': form,
        }
    
    return render(request, 'test_app/detail.html', context)


def confirm_contact(request, pk):
    visitor = Visitors.objects.get(pk=pk)
    
    form = MemberForm(request.POST)
    if form.is_valid():
        interviewer = form.cleaned_data['member']
    if request.method == 'POST':
        context = {
            'visitor': visitor,
            'interviewer': interviewer,
            'time': request.POST.get('time'),
            'contents': request.POST.get('contents'),
        }
    return render(request, 'test_app/confirm_contact.html', context)



def sent_contact(request, pk):
    visitor = Visitors.objects.get(pk=pk)
    visitor.save()
    if request.method == 'POST':
        contact = visitor
        interviewer_post_name = request.POST.get('interviewer')
        print(interviewer_post_name)
        target = '/'
        idx = interviewer_post_name.find(target)
        interviewer_name = interviewer_post_name[idx+2:]
        print(interviewer_name)
        if interviewer_post_name == "None":
            interviewer = None
        else:
            interviewer = Member.objects.get(name=interviewer_name)
            visitor.is_contacted = True
        time = request.POST.get('time')
        if time == "":
            time = '00:00'
        contents = request.POST.get('contents')
        try:
            contact = Contact.objects.get(contact_id=pk)
            contact.interviewer = interviewer
            contact.time = time
            contact.contents = contents
        except:
            Contact.objects.create(contact=contact, interviewer=interviewer, time=time, contents=contents)

    return render(request, 'test_app/lazy/thankyou_contact.html')


"""
UpdateとDelete
"""
class VisitorsUpdate(UpdateView):
    template_name = 'test_app/update_visitors.html'
    form_class = VisitorsForm
    model = Visitors
    
    def get_success_url(self):
        messages.info(self.request, f'訪問者情報を更新しました！')
        return reverse_lazy('test_app:detail', kwargs={'pk': self.kwargs['pk']})


class ContactUpdate(UpdateView):
    template_name = 'test_app/update_contact.html'
    form_class = ContactForm
    model = Contact

    def get_success_url(self, **kwargs):
        messages.info(self.request, f'担当者情報を更新しました！')
        return reverse_lazy('test_app:detail', kwargs={'pk': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['visitor'] = Visitors.objects.get(pk=self.kwargs['id'])
        return context


# class ContactAllUpdate(UpdateView):
#     template_name = 'test_app/update_contact.html'
#     form_class = VisitorsForm
#     model = Visitors

#     def get_success_url(self):
#         return reverse_lazy('test_app:detail', kwargs={'pk': self.kwargs['pk']})

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     context['visitor'] = Visitors.objects.get(pk=self.kwargs['id'])
    #     return context


# from extra_views import InlineFormSetView, UpdateWithInlinesView


# class ContactInlineFormSet(InlineFormSetView):
#     model = Contact
#     fields = ("interviewer", "time", "contents")
#     can_delete = True

# class VisitorsContactUpdateFormSetView(UpdateWithInlinesView):
#     model = Visitors
#     fields = ('date', 'time', 'company_name', 'visitor_name', 'temperature',
#                 'accompany1_name', 'accompany1_temp', 'accompany2_name', 'accompany2_temp',
#                 'accompany3_name', 'accompany3_temp', 'position', 'interviewer', 'content',
#                 'is_contacted')
#     inlines = [ContactInlineFormSet, ]
#     template_name = "test_app/update_contact.html"
    
#     def get_success_url(self):
#         return reverse_lazy('test_app:detail', kwargs={'pk': self.kwargs['pk']})





def update_allpost(request, pk):
    visitors = get_object_or_404(Visitors, pk=pk)
    form = VisitorsForm(request.POST or None, instance=visitors)
    ContactFormset = forms.inlineformset_factory(
            Visitors, Contact, fields=('interviewer', 'time', 'contents'),
            can_delete=False,
            widgets={
                'interviewer': forms.Select(attrs={'class': 'form-control'}),
                'time': forms.TimeInput(attrs={'class': 'form-control'}),
                'contents': forms.Textarea(attrs={'class': 'form-control'}),
            }
        )
    formset = ContactFormset(request.POST or None, instance=visitors)  # 今回はファイルなのでrequest.FILESが必要
    if request.method == 'POST' and form.is_valid():
        form.save()
        print('POSTメソッド')
        print(formset.errors)
        print()
        if formset.is_valid():
            print('formset.save()')
            formset.save()
            return redirect('test_app:detail', pk=pk)
    else:
        print('POSTメソッドだけども・・・')

    # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納
    context = {
        'form': form,
        'formset': formset,
    }
    print(formset)
    print('GETメソッド')
    return render(request, 'test_app/update_allpost.html', context)