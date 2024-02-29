from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting , register_setting
# Create your models here.
# BaseGenericSetting should be changed to BaseSiteSetting but I can't figure out how to get the current site when consuming the settings
# JanR 2024-02-20
@register_setting
class MFImageAppConfig(BaseGenericSetting):
    server_id = models.CharField(
        max_length=255, help_text='Mediaflow ServerID')
    server_key = models.CharField(
        max_length=255, help_text='Mediaflow ServerKey')
