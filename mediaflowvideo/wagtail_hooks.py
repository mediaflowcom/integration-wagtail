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


@hooks.register('after_publish_page')
def after_publish_page(request, page):
    # Call the process_data method on the page
    print("page published")
    #print(page.specific.media)
    for field in page.specific._meta.fields:
        name = str(field)
        try:
            check = name[name.rindex(".")+1:]
        except:
            break
        if (not "wagtailcore" in name) and (not "page_ptr" in check):
            val = str(getattr(page.specific, check, None))
            s = val.find("data-mf-file-id")
            if s > 0:
                begin = s+17
                end = begin + val[begin:].index('"')
                id_image = val[begin:end]
                print("found", id_image)
                # here is your id_Image to report usage on
                # get the server key from MFVideoAppConfig to gain an api token and perform ajax request to register usage                 
                # this is for videoblocks only.. look into how we can check for image updates in the rich text editor..


        
