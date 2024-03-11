from .views import mfvideo_modal
from .draftail import VideoEntityElementHandler, video_entity_decorator
from django.urls import path
from wagtail import hooks
from django.utils.html import format_html
from .models import MFVideoAppConfig
import requests
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
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
                




@hooks.register('register_rich_text_features')
def register_help_text_feature(features):
    """
    Registering the `mf-video` feature, which uses the `mf-video` Draft.js block type,
    and is stored as HTML with a `<div class="mf-video">` tag.
    """
    feature_name = 'mf-video'
    type_ = 'mf-video'

    control = {
        'type': type_,
        'icon': 'media',
        'description': 'Mediaflow Video',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['mf-video.css']}, js=['js/draftail-videoblock.js'])
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'iframe[class=mf-video]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'iframe', 'props': {'class': 'mf-video'}}}},
    })

        
@hooks.register('register_rich_text_features')
def register_video_feature(features):
    features.default_features.append('mf-video')
    """
    Registering the `stock` feature, which uses the `STOCK` Draft.js entity type,
    and is stored as HTML with a `<span data-stock>` tag.
    """
    feature_name = 'mf-video'
    type_ = 'MF_VIDEO'

    control = {
        'type': type_,
        'label': '$',
        'description': 'Mediaflow video',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/draftail-videoblock.js'],
            css={'all': ['css/stock.css']}
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        'from_database_format': {'iframe[class=mf-video]': VideoEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: video_entity_decorator}},
    })
