from django.urls import path
from . import views

app_name = 'test_app'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('confirm/', views.confirm, name='confirm'),
    path('thankyou/', views.sent, name='sent'),
    path('history/', views.history, name='history'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('confirm_contact/<int:pk>/', views.confirm_contact, name='confirm_contact'),
    path('sent_contact/<int:pk>/', views.sent_contact, name='sent_contact'),

    path('update_visitors/<int:pk>/', views.VisitorsUpdate.as_view(), name='update_visitors'),
    path('update_contact/<int:pk>/<int:id>', views.ContactUpdate.as_view(), name='update_contact'),
    path('update_contact_all/<int:pk>/', views.VisitorsContactUpdateFormSetView.as_view(), name='update_contact_all'),
]