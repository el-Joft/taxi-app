from django.contrib import admin
from django.urls import path

from trips.views import SignUpView

app_name = 'trips'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('sign_up/', SignUpView.as_view(), name='sign_up'),
]
