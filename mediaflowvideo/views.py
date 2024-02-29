from django.shortcuts import render
from wagtail.admin.modal_workflow import render_modal_workflow
from .models import MFVideoAppConfig

# Create your views here.
def mfvideo_modal(request):

    appSettings = MFVideoAppConfig.load(request_or_site=request)
    return render_modal_workflow(
        request,
        'mediaflowvideo/mf-video-modal.html', # html template
        None,
        {'trigger': request.GET.get('trigger'), "server_key": appSettings.server_key, "server_id": appSettings.server_id}, # html template vars
        json_data={'step': 'choose'}
    )
