from wagtail.blocks.struct_block import StructBlock,StructValue
from wagtail.blocks import CharBlock,BooleanBlock, IntegerBlock,ChoiceBlock
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from django import forms
from django.db import models
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseGenericSetting , register_setting
from django.db import models
import requests
# BaseGenericSetting should be changed to BaseSiteSetting but I can't figure out how to get the current site when consuming the settings
# JanR 2024-02-20
@register_setting
class MFVideoAppConfig(BaseGenericSetting ):
    server_id = models.CharField(
        max_length=255, help_text='Mediaflow ServerID')
    server_key = models.CharField(
        max_length=255, help_text='Mediaflow ServerKey')


class MFVideoblockValue(StructValue):   
    def __init__(self, block, *args):                
        self.element_id = get_random_string(length=10,allowed_chars='abcdefghijklmnopqrstuvwxyz')              
        super().__init__(self,*args)

   
    @cached_property
    def get_video_data(self):               
        r = requests.get('https://m.mediaflow.com/json/' + self.get("media_id"), headers={'Accept': 'application/json'})        
        return r.json()

    @property    
    def random_element_id(self):               
        return self.element_id

    @property    
    def src(self):               
        s_param = ""
        m_id = self.get("media_id")
        if self.get("autoplay"):
            s_param = s_param + "autoplay=1&"
        if self.get("start_offset") > 0:
            s_param = s_param + "start=" + str(self.get("start_offset")) + "&"
        if s_param == "":
            return "//play.mediaflowpro.com/ovp/11/" + m_id
        else:
            return "//play.mediaflowpro.com/ovp/11/" + m_id + "?" + s_param[:-1]

    @property    
    def name(self):
        try:               
            title = (self.get_video_data)["title"]
        except:
            title = ""
        return title
    
    @property    
    def poster(self):
        try:               
            p = (self.get_video_data)["poster"]
        except:
            p = "https://assets.mediaflowpro.com/a/ee80c59d46c348ff4bb07b8294d5fad4/poster.jpg"
        return p


class MfVideoBlock(StructBlock):
    media_id = CharBlock(help_text='Media ID')
    autoplay = BooleanBlock(help_text='Start playback automatically if possible', default=False,required =False)
    file_id = IntegerBlock(default=0,required =False)
    folder_id = IntegerBlock(default=0,required =False)
    start_offset = IntegerBlock(help_text='Start playback at n seconds into the movie', default=0,required =False)
    embed_method = ChoiceBlock(choices=[
        ('iframe', 'IFrame'),
        ('js', 'Javascript'),
    ], icon='embed', help_text='Embed method', default='js',required =False)
    
    def get_form_context(self, value, prefix='', errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)        
        return context

    class Meta:
        template = 'mediaflowvideo/mf-video-block.html'
        icon = "media"
        admin_text = mark_safe("<b>Image Block</b>")
        label = "Mediaflow Video Block"
        value_class = MFVideoblockValue
        form_template = 'mediaflowvideo/mf-video-form.html'
    class Media:
        js = ('js/customer_detail.js',)




class MountVideoAdapter(StructBlockAdapter):
    js_constructor = "mediaflowvideo.MfVideoBlock"

    @cached_property
    def media(self):
        structblock_media = super().media        
        return forms.Media(
            js=structblock_media._js + ["js/mfvideoblock-telepath.js"],
            #css={"all": ("css/mount-video.css",)},
        )

register(MountVideoAdapter(), MfVideoBlock)
