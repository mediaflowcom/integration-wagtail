from .views import mfvideo_modal
from django.urls import path
from wagtail import hooks
from django.utils.html import format_html
from .models import MFVideoAppConfig
import requests

@hooks.register('register_admin_urls')
def register_mfvideo_urls():    
    return [
        path('mfvideomodal/', mfvideo_modal, name='Mediaflow Video Selector'),
    ]


@hooks.register('insert_editor_js')
def fileselector_js():    
    return format_html('<script src="https://mfstatic.com/js/fileselector.min.js"></script>')


@hooks.register('after_publish_page')
def after_publish_page(request, page):
    # Call the process_data method on the page
    print("page published")
    #print(page.specific.media)
    for field in page.specific._meta.fields:
        name = str(field)
        try:
            short_name = name[name.rindex(".")+1:]
        except:
            break
        if (not "wagtailcore" in name) and (not "page_ptr" in short_name):
            val = str(getattr(page.specific, short_name, None))
            attr_start_pos = val.find("data-mf-file-id")
            if attr_start_pos > 0:
                try:
                    begin = attr_start_pos + 17
                    end = begin + val[begin:].index('"')
                    id_image = val[begin:end]
                    appSettings = MFVideoAppConfig.load(request_or_site=request)                
                    req = requests.get('https://api.mediaflow.com/1/oauth2/token?client_id=8b62ca84&client_secret=rZpA0vP7oKOSJw3lZBX1e4EVElHsbQ&grant_type=refresh_token&refresh_token=' + 
                      appSettings.server_key, headers={'Accept': 'application/json'})
                    token = req.json()["access_token"]
                    web = { 'page': page.full_url, 'pageName': page.title}
                    post_data = {'contact': str(page.owner), "types": ['web'], 'web': web, 'project': str(page.get_site()), 'date': str(page.last_published_at)}
                    req = requests.post('https://api.mediaflow.com/1/file/' + str(id_image) + '/usage?access_token=' + token, json=post_data, headers={'Accept': 'application/json'})
                except:
                    break
                



        
