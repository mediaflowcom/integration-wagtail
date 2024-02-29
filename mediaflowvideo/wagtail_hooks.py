from .views import mfvideo_modal
from django.urls import path
from wagtail import hooks
from django.utils.html import format_html

@hooks.register('register_admin_urls')
def register_mfvideo_urls():    
    return [
        path('mfvideomodal/', mfvideo_modal, name='Mediaflow Video Selector'),
    ]


@hooks.register('insert_editor_js')
def fileselector_js():    
    return format_html('<script src="https://mfstatic.com/js/fileselector.min.js"></script>')
