from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'mailing', MailingViewSet, basename="mailing")
router.register(r'client', ClientViewSet, basename="client")

api_urls = router.urls
