from turtle import position
from django.shortcuts import get_object_or_404, render
from ..models import *
from django.urls import reverse_lazy
from ..forms import ContactForm, MemberForm, VisitorsForm
from django.views.generic import UpdateView, DeleteView
from django import forms
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

# Create your views here.


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


"""
Delete機能
"""
class ContactDelete(DeleteView):
        
    model = Contact
    template_name = 'test_app/delete_contact.html'
    success_url = reverse_lazy('test_app:history')

    def get_success_url(self):
        return reverse('test_app:history', kwargs={'page': '1'})

    def get(self, request, *args, **kwargs):
        visitor = Visitors.objects.get(contact = self.kwargs['pk'])
        contact = Contact.objects.get(id=self.kwargs['pk'])
        print('DeleteView/getメソッド')
        print(contact)
        print(contact.id)
        print(visitor)
        print(visitor.id)
        print(visitor.is_contacted)
        contact = Contact.objects.get(pk=self.kwargs['pk'])
        context = {
            'contact': contact,
        }
        return render(request, 'test_app/delete_contact.html', context)

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        # visitor = Visitors.objects.get(contact = self.kwargs['pk'])
        # print(visitor)
        # print(visitor.id)
        # print(visitor.is_contacted)
        # visitor.is_contacted = False
        # print(visitor.is_contacted)
        # visitor.save()
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

    def post(self, request, *args, **kwargs):
        visitor = Visitors.objects.get(contact = self.kwargs['pk'])
        print(visitor)
        print(visitor.id)
        print(visitor.is_contacted)
        visitor.is_contacted = False
        print(visitor.is_contacted)
        visitor.save()
        return self.delete(request)


class VisitorsDelete(DeleteView):

    model = Visitors
    template_name = 'test_app/delete_contact_all.html'
    success_url = reverse_lazy('test_app:history')

    def get_success_url(self):
        return reverse('test_app:history', kwargs={'page': '1'})
    
    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        # visitor = Visitors.objects.get(contact = self.kwargs['pk'])
        # print(visitor)
        # print(visitor.id)
        # print(visitor.is_contacted)
        # visitor.is_contacted = False
        # print(visitor.is_contacted)
        # visitor.save()
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

    def form_valid(self, form):
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return super().form_valid(form)