
from django.db import models
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseGenericSetting , register_setting
from wagtail.images.models import AbstractImage
from django.template.loader import render_to_string
from django.utils.functional import cached_property

from wagtail.admin.compare import BlockComparison
from wagtail.images.blocks import ImageChooserBlock

from wagtail.images.shortcuts import get_rendition_or_not_found
