from django.forms import FileInput

from mediaflowimage.models import MFImageAppConfig


class MedialowFileInput(FileInput):
    template_name = "widgets/fileinput-image.html"


    def get_context(self, name, value, attrs):
        appSettings = MFImageAppConfig.load()
        context = super(FileInput, self).get_context(name, value, attrs)
        context.update({'server_key': appSettings.server_key })
        return context


    class Media:       
        js = ["js/fileinput-image.js"]
