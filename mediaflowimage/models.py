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




# models.py
from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class MfImage(AbstractImage):
    # Add any extra fields to image here

    # To add a caption field:
    photographer = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    mediaflow_id = models.IntegerField(blank=True,default=0)


    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'description','photographer','mediaflow_id'
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(MfImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
                 ('image', 'filter_spec', 'focal_point_key'),
        )
