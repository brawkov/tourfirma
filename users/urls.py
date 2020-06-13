from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from .views import SignUpView, show_admin_custom_page

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    url(r'^admin-custom-page/$', user_passes_test(lambda u: u.is_superuser)(show_admin_custom_page), name='show_admin_custom_page'),
]


