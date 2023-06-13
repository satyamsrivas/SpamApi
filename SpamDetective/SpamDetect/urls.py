
from django.urls import path,include
from SpamDetect import views

urlpatterns = [
    path('register_user', views.register_user),
    path('mark_as_spam',views.mark_as_spam),
    path('search_by_name',views.search_by_name),
    path('search_by_phone_number',views.search_by_phone_number),
    path('display_details',views.display_details),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),

]
