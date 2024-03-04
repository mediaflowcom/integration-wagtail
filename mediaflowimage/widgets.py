from django.forms import FileInput

from mediaflowimage.models import MFImageAppConfig


# This widget is used by the Image Form 'MfImageForm'
class MedialowFileInput(FileInput):
    template_name = "widgets/mf-custom-imageinput.html"

    def get_context(self, name, value, attrs):
        appSettings = MFImageAppConfig.load()
        context = super(FileInput, self).get_context(name, value, attrs)
        context.update({'server_key': appSettings.server_key })
        return context

    class Media:       
        js = ["js/mf-imagechooser-extensions.js"]
