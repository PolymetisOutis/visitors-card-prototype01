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
from django.core.paginator import Paginator, EmptyPage


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

def welcome_widget(request):
    form = VisitorsForm()
    print(form)
    print(dir(form))
    context = {
        'form': form,
    }
    return render(request, 'test_app/entry_form/welcome_widget.html', context)


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


def history(request, page=1):
    visitors = Visitors.objects.all().order_by('-id')
    contact_objects = Contact.objects.all()
    interviewer = Member.objects.all()
    posts = Post.objects.all()


    """
    検索機能　SearchForm
    """
    if request.method == 'POST':
        print('history POST method')
        keyword = request.POST.get('search_form')
        if keyword:
            posted_visitors = visitors
            posted_interviewer = interviewer
            posted_contact_objects = contact_objects
            keyword = keyword.split()
            for k in keyword:
                visitors = visitors.filter(
                            Q(date__icontains=k) |
                            Q(time__icontains=k) |
                            Q(company_name__icontains=k) |
                            Q(visitor_name__icontains=k) |
                            Q(temperature__icontains=k) |
                            Q(accompany1_name__icontains=k) |
                            Q(accompany1_temp__icontains=k) |
                            Q(accompany2_name__icontains=k) |
                            Q(accompany2_temp__icontains=k) |
                            Q(accompany3_name__icontains=k) |
                            Q(accompany3_temp__icontains=k) |
                            Q(position__icontains=k) |
                            Q(interviewer__icontains=k) |
                            Q(content__icontains=k)
                            # Q(contact__interviewer__post__icontains=k) |
                            # Q(contact__interviewer__name__icontains=k) |
                            # Q(contact__time__icontains=k) |
                            # Q(contact__contents__icontains=k)
                )
                contact_objects = contact_objects.filter(
                        # Q(interviewer_name__icontains=k) |
                        # Q(interviewer_post__icontains=k) |
                        Q(time__icontains=k) |
                        Q(contents__icontains=k)
                    )
                interviewer = interviewer.filter(
                    name=k
                )
                posts = posts.filter(
                    name=k
                )

            if posts:
                print('if posts')
                print(posts)
                list_of_ids = set([post.pk for post in posts])
                interviewer |= posted_interviewer.filter(post_id__in=list_of_ids)
                print('if posts')
                print(interviewer)
            
            if interviewer:
                print('if interviewer')
                print(interviewer)
                list_of_ids = set([interviewer_object.pk for interviewer_object in interviewer])
                print(list_of_ids)
                list_of_ids = list(list_of_ids)
                print(list_of_ids)
                contact_objects |= posted_contact_objects.filter(interviewer_id__in=list_of_ids)
                print('if interviewer')
                print(contact_objects)
            
            if contact_objects:
                print('if contact_objects')
                print(contact_objects)
                list_of_ids = set([contact_object.contact.pk for contact_object in contact_objects])
                print(list_of_ids)
                visitors |= posted_visitors.filter(id__in=list_of_ids)


                print('if contact_objects')
                print(visitors)
                print('Contact contact テスト')
                test_obj = Contact.objects.filter(contents__icontains='緑茶')[0]
                print(test_obj.contact.pk)
                test_visitor = Visitors.objects.filter(id=test_obj.contact.pk)
                print(test_visitor)
                print('Contact contact テスト2')
                test_list = [test_obj.contact.pk]
                print(test_list)
                test_visitor2 = Visitors.objects.filter(id__in=test_list)
                print(test_visitor2)
        visitors = visitors.distinct()
        print(visitors)
    """
    検索機能ここまで
    """
    """
    ページネーション
    """
    paginator = Paginator(visitors, 6)

    try:
        visitors = paginator.page(page)
    except EmptyPage:
        visitors = paginator.page(paginator.num_pages)

    # visitor2 = Visitors.objects.get(id=2)
    # print(dir(visitor2.contact))
    context = {
        'visitors': visitors,
    }

    """
    統計情報に向けたテスト
    """
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
    """
    もしPOSTメソッドならば
    """
    if request.method == 'POST':
        contact = visitor # これ要らない気がすると思って一度消したけど、最後のcreate文で代入してデータベースに登録している。
        interviewer_post_name = request.POST.get('interviewer')
        print(interviewer_post_name)
        target = '/'
        idx = interviewer_post_name.find(target) # target:'/'のindex位置を取得
        interviewer_name = interviewer_post_name[idx+2:] # target:'/'の位置からプラス2した位置から文字列取得
        print(interviewer_name)
        """
        もし名前を何も選ばずに担当者が登録したら
        """
        if interviewer_post_name == "None":
            interviewer = None
        else:
            interviewer = Member.objects.get(name=interviewer_name)
            visitor.is_contacted = True
            visitor.save()
        time = request.POST.get('time')
        """
        もし時刻を何も入れずに担当者が登録したら
        """
        if time == "":
            time = '00:00'
        contents = request.POST.get('contents')
        
        try:
            contact = Contact.objects.get(contact_id=pk) # VisitorsのidとはContactのcontactのidとなる。
                                                         # Visitorsのidがpkの場合のContactのデータを取得している。
                                                         # try文なので、エラー、即ち、is_contacted=Falseで尚且つ、
                                                         # Contactのデータが無ければexcept文が実行される。
            contact.interviewer = interviewer
            contact.time = time
            contact.contents = contents
            contact.save() # データベースへの反映.save()が抜けていたので付け足した。
        except:
            Contact.objects.create(contact=contact, interviewer=interviewer, time=time, contents=contents)

    return render(request, 'test_app/lazy/thankyou_contact.html')

