from wagtail import hooks
from django.utils.html import format_html
from django.utils.safestring import mark_safe


@hooks.register('insert_editor_js')
def fileselector_js():    
    return format_html('<script src="https://mfstatic.com/js/fileselector.min.js"></script>') + mark_safe(
            """
            <script>            
                window.addEventListener('DOMContentLoaded', (event) => {
                    let prevChooseHandler = window.IMAGE_CHOOSER_MODAL_ONLOAD_HANDLERS.choose;                    
                    window.IMAGE_CHOOSER_MODAL_ONLOAD_HANDLERS.choose = (e,t) => {
                        window.mfImageModal = e;                             
                        prevChooseHandler(e,t);                        
                    }                    
                });
            </script>
            """
        )
