from django.shortcuts import render
from wagtail.admin.modal_workflow import render_modal_workflow
from .models import MFVideoAppConfig
from django.conf import settings
# Create your views here.
def mfvideo_modal(request):

    appSettings = MFVideoAppConfig.load(request_or_site=request)
    client_id = getattr(settings, "MEDIAFLOW_CLIENT_ID", "")
    client_secret = getattr(settings, "MEDIAFLOW_CLIENT_SECRET", "")
    print("client_secet", client_secret)
    return render_modal_workflow(
        request,
        'mediaflowvideo/mf-video-modal.html', # html template
        None,
        {'trigger': request.GET.get('trigger'), "client_secret": client_secret, "client_id": client_id, "server_key": appSettings.server_key, "server_id": appSettings.server_id}, # html template vars
        json_data={'step': 'choose'}
    )
