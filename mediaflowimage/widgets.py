from django.forms import NumberInput
from django.conf import settings

from mediaflowimage.models import MFImageAppConfig


# This widget is used by the Image Form 'MfImageForm'
class MedialowFileInput(NumberInput):
    template_name = "widgets/mf-custom-imageinput.html"

    def get_context(self, name, value, attrs):
        appSettings = MFImageAppConfig.load()
        context = super(NumberInput, self).get_context(name, value, attrs)
        context.update({'server_key': appSettings.server_key })
        context.update({'client_id': getattr(settings, "MEDIAFLOW_CLIENT_ID", "") })
        context.update({'client_secret': getattr(settings, "MEDIAFLOW_CLIENT_SECRET", "") })
        return context

    class Media:       
        js = ["js/mf-imagechooser-extensions.js"]
