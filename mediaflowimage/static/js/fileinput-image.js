// This is the js-file that is used by our custom FileInput widget import_button.html
// the widget is a django FileInput with an extra button to open 
// 'Insert from Mediaflow' modal

$(document).ready(function() {

   

    function useImage(id) {
        
        var el = document.getElementById('mf-use-link');
        el.href += id + '/';
        el.click();
    }
    
  
    function uploadToWagtail(imageFile, title) {
      let formData = new FormData();
      const el = document.querySelector('[name=collection-selector]');
      
      formData.append("image-chooser-upload-title", title);
      formData.append("image-chooser-upload-collection", "1");
      formData.append("image-chooser-upload-file", imageFile);
      formData.append("image-chooser-upload-tags", '');
      formData.append("image-chooser-upload-focal_point_x", '0');
      formData.append("image-chooser-upload-focal_point_y", '0');
      formData.append("image-chooser-upload-focal_point_width", '20');
      formData.append("image-chooser-upload-focal_point_height", '20');
      var request = new XMLHttpRequest();
      request.addEventListener("load", async (e) => {
        let res = await request.response;
        res = JSON.parse(res);
        if (res && res.step == 'chosen') {
            console.log('media uploaded! id:',res.result.id)
            useImage(res.result.id);            
        }
        if (res && res.step == 'duplicate_found') {
            document.getElementById('mf-fileselector').innerHTML = res.htmlFragment;
        }
        
      });
      request.addEventListener("error", async (e) => {
       //
      });
      
      var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      request.open("POST", "/admin/images/chooser/create/");
      request.setRequestHeader("X-CSRFToken", csrfToken);
      request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
      request.send(formData);
  }
  
    function startImport(downloadURL, title) {
        var imageRequest = new XMLHttpRequest();
        imageRequest.addEventListener("load", (e) => {
          
          uploadToWagtail(
            new File([imageRequest.response], title + ".jpg"), title);
        });
        imageRequest.addEventListener("error", () => {          
        });
        imageRequest.addEventListener("progress", (e) => {
  
        });
        imageRequest.open(
          "GET",
          downloadURL
        );
        imageRequest.responseType = "blob";        
        imageRequest.send();
      }

    server_key = document.getElementById('mf-insert-button').getAttribute('data-server-key');
    var tabLink = document.createElement('a');
    tabLink.innerText = 'Insert from Mediaflow';
    tabLink.href = '#tab-mfp-insert';
    tabLink.id = 'tab-label-mfp-insert';
    tabLink.className = 'w-tabs__tab';
    var myFileSelector = null;
    var el = document.querySelector('.modal-body [role=tablist]');
    tabLink.addEventListener('click', function(e) {
        e.preventDefault();
        for(var s of document.querySelectorAll('.modal-body section')) {
            
            if (s.id == 'tab-mfp-insert') {
                console.log('removing hidden attr');
               s.removeAttribute('hidden');
            }
            else {
                s.setAttribute('hidden','');
            }
               
        }
        if(myFileSelector) {
            return;
        }
        
        myFileSelector = new FileSelector('mf-fileselector', {
            auth: 'token',
            client_id: '8b62ca84',
            client_secret: 'rZpA0vP7oKOSJw3lZBX1e4EVElHsbQ',
            refresh_token: server_key,
            showDoneButton: false,
            limitFileType: 'jpg',
            viewLayout: 'thumbnails',
            allowCrop: true,
            noCropButton:false,
            showDoneButton: true,
            locale: 'sv-se',
            downloadFormat: 'original',
            ready: function() {
              
            },
            success: function(o) {              
              startImport(o.url, filename);        
            },
            events: function(eventName, eventData) {
                if(eventName === 'fileClick') {
                  validOK = true;    
                  filename = eventData.name;
                  console.log(eventData);
                  
                }
                if(eventName === 'folderClick') {
                  validOK = false;
                  
      
                }
            }      
          });     
    })
    var s = document.createElement('section');
    s.role = 'tabpanel';
    s.className = 'w-tabs__panel';
    s.id = 'tab-mfp-insert';
    s.setAttribute('hidden','');    
    document.querySelector('.modal-body .tab-content').appendChild(s);    
    el.appendChild(tabLink);
    console.log(el);
    el = document.createElement('div');
    el.id = 'mf-fileselector';
    el.className = 'light';
    el.style.position = 'relative';
    el.style.minHeight = '460px';
    s.appendChild(el);

    
    for(var s of document.querySelectorAll('.modal-body a.w-tabs__tab')) {
        if (s.id != 'tab-label-mfp-insert') {
            console.log('setting click handler for ' , s);
            s.addEventListener('click', function() {
                document.getElementById('tab-mfp-insert').setAttribute('hidden','');
            })
        }
        
    }

});
