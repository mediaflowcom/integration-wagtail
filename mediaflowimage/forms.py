from wagtail.admin.views.generic.chooser import CreationFormMixin
from wagtail.images.forms import BaseImageForm
from django.utils.translation import gettext as _
from .widgets import MedialowFileInput


        
class MfImageForm(BaseImageForm, CreationFormMixin):
    class Meta:   
        # Override the widget for the 'file' field
        # so that we can inject our own behaviour
        widgets = {
            "file":  MedialowFileInput()
        }
