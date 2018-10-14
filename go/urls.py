from django.urls import path
from . import views
from . import simple_views

urlpatterns = [
    path('',simple_views.search),
    path('sign-in/',views.sign_in),
    path('sign-up/',views.sign_up),
    path('user/',views.user),
    path('sign-out/',views.sign_out),
    path('password/',views.change_password),
    path('choose-level/',views.choose_level),
    path('email/',views.change_email),
    path('faq/',simple_views.faq),
    path('contact-us/',simple_views.contact_us),
    path('new-items/',views.new_item),
    path('forget-pass/',views.forget_pass),
    path('payment/',views.payment),
    path('<str:item>/<path:api>/',simple_views.show_item)
]