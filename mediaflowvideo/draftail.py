from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from django.utils.crypto import get_random_string

def video_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the video entities into an iframe tag.
    """

    s_param = ""
    src = ""
    m_id = props['mediaId']
    if props["autoPlay"] == '1':
        s_param = s_param + "autoplay=1&"
    if props["startOffset"] != '0':
        s_param = s_param + "start=" + str(props["startOffset"]) + "&"
    if s_param == "":
        src = "//play.mediaflowpro.com/ovp/11/" + m_id
    else:
        src = "//play.mediaflowpro.com/ovp/11/" + m_id + "?" + s_param[:-1]
   
    return DOM.create_element('iframe', {
        'class': 'mf-video',
        'src': src,        
        'data-mediaid': props['mediaId'],
        'data-embed-method': props['embedMethod'],
        'data-auto-play': props['autoPlay'],
        'data-start-offset': props['startOffset']
    }, props['children'])
class VideoEntityElementHandler(InlineEntityElementHandler):    
    mutability = 'MUTABLE'

    def get_attribute_data(self, attrs):       
        print('attrs', attrs)
        return { 'mediaId': attrs['data-mediaid'],
                 'embedMethod': attrs['data-embed-method'],                 
                 'autoPlay': attrs['data-auto-play'],                 
                 'startOffset': attrs['data-start-offset'],                 
               }
