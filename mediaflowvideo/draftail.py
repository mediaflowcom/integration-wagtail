from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

def video_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the video entities into a span tag.
    """
    if props['embedMethod'] == 'iframe':
        return DOM.create_element('iframe', {        
            'src': 'https://play.mediaflowpro.com/ovp/11/' + props['mediaId'],        
            'data-media-id': props['mediaId'],
            'data-embed-method': props['embedMethod'],
        }, props['children'])
    
    # it is possible to return an element with children, as in <div> <srcipt> etc.. look into that!
    return DOM.create_element('div', {        
            'data-media-id': props['mediaId'],
            'data-embed-method': props['embedMethod'],
        }, props['children'])


class VideoEntityElementHandler(InlineEntityElementHandler):    
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):       
        return { 'mediaId': attrs['data-media-id'],
                 'embedMethod': attrs['data-embed-method'],
               }
