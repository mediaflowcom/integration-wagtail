from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

def video_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the video entities into a span tag.
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
    if props['embedMethod'] == 'iframe':
        return DOM.create_element('iframe', {        
            'src': src,        
            'data-media-id': props['mediaId'],
            'data-embed-method': props['embedMethod'],
            'data-auto-play': props['autoPlay'],
            'data-start-offset': props['startOffset']
        }, props['children'])
    
    # it is possible to return an element with children, as in <div> <srcipt> etc.. look into that!
    return DOM.create_element('div', {        
            'data-media-id': props['mediaId'],
            'data-embed-method': props['embedMethod'],
            'data-auto-play': props['autoPlay'],
            'data-start-offset': props['startOffset']
        }, DOM.create_element('script', { 'src': props['mediaId']}))


class VideoEntityElementHandler(InlineEntityElementHandler):    
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):       
        return { 'mediaId': attrs['data-media-id'],
                 'embedMethod': attrs['data-embed-method'],                 
                 'autoPlay': attrs['data-auto-play'],                 
                 'startOffset': attrs['data-start-offset'],                 
               }
