from django.contrib import admin
from django.urls import path
from duplicates.views import FindDuplicates

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FindDuplicates.as_view()),
]
