

# Setting up for development/testing locally

*The setup follows the guide published here: https://docs.wagtail.org/en/stable/getting_started/tutorial.html
but with a few extra steps that are documented below.*

## Install python 3
https://www.python.org/downloads/

## Create and activate a virtual environment (recommended)
    py -m venv mysite\env
    mysite\env\Scripts\activate.bat
 
If mysite\env\Scripts\activate.bat doesn't work, run:  

    mysite\env\Scripts\activate
  
## Install wagtail 4.2
    pip install wagtail==4.2
## Generate a site
    wagtail start mysite mysite
## Install project dependencies
    cd mysite
    pip install -r requirements.txt
## Create the database
    python manage.py migrate
## Create an admin user
    python manage.py createsuperuser
## Install the plugins (manual installation)

* Copy the folders "mediaflowvideo" and "mediaflowimage" to the root folder of the project

### Edit the settings file (mysite/settings/base.py:

 - Add **"wagtail.contrib.settings", "mediaflowvideo", "mediaflowimage"** to the array **INSTALLED_APPS** (near the top of the file)

- Add "mf-video" to the feature list for the Draftail Rich Text Editor as shown below. (Create the variable if it does not exist in base.py):

      WAGTAILADMIN_RICH_TEXT_EDITORS = {
      	'default': {
      		'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
      		'OPTIONS': {
      			'features': ['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr','mf-video']
      		}
      	}
      }

- Tell Wagtail to use our custom image form (Create the variable if it does not exist in base.py)

    WAGTAILIMAGES_IMAGE_FORM_BASE = 'mediaflowimage.forms.MfImageForm'

 
## Create a demo page with images and video

Following the tutorial here: https://docs.wagtail.org/en/stable/getting_started/tutorial.html#extend-the-homepage-model but instead change the contents of home/models.py to:


    from wagtail.images.blocks import ImageChooserBlock
    from wagtail.models import Page
    from wagtail.fields import RichTextField,StreamField
    from wagtail.admin.panels import FieldPanel
    from mediaflowvideo.models import MfVideoBlock
    
    class HomePage(Page):
        text = RichTextField(blank=False, default="")           
        media = StreamField([        
            ('video', MfVideoBlock(required=False)),
            ('image', ImageChooserBlock(required=False))
        ], use_json_field=True,  default=[])
      
        content_panels = Page.content_panels + [
            FieldPanel('text'),   
            FieldPanel("media"),
        ]

  ... and change the contents of home/templates/home_page.html to:

    {% extends "base.html" %}
    {% load wagtailcore_tags %}
    {% block body_class %}template-homepage{% endblock %}
    {% block content %}    
    	<div style="max-width:640px">
    		{{ page.text|richtext }}
    		{% include_block page.media %}
    	</div>
    {% endblock %}

 
## Perform db migrations
    python manage.py makemigrations
    python manage.py migrate

## Start server
    python manage.py runserver 
  
## Log into the admin interface
    http://localhost:8000/admin
  There you should now have two new menu items under the Settings tab: '**Mf image app config**' and '**Mf video app config**'. Enter a valid server key (server id is not currently used so it does not matter what you enter here at the moment). The server key is the 10 digits long string consisting of uppercase letters and numbers. You may use an existing server key for another CMS, such as Sitevision or Drupal for testing purposes.

Now you can try editing the startpage or creating new pages. The "Home Page" page type has a Rich Text field for testing image/video embeds into Draftail, and a StreamField block that can contain any amount of Image blocks and Video blocks.

## When done developing

    mysite\env\Scripts\deactivate.bat 

or

    mysite\env\Scripts\deactivate
